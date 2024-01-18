from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from ..exceptions import MissingMailConfirmationError
from ..models import Account
from .serializers import (
    LoginWithCredentialsSerializer,
    PublicAccountDataSerializer,
    RegisterAccountSerializer,
    UpdateAccountSerializer,
    VerifyAccountSerializer,
    ChangePasswordSerializer,
    ChangePasswordRequestSerializer,
    PasswordResetRequestModel,
)


class PublicAccountDataView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Account.objects.all()
    serializer_class = PublicAccountDataSerializer


class LoginWithTokenView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        if request.auth is None:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return super().post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        try:
            if not request.user.is_active:
                raise MissingMailConfirmationError()
        except MissingMailConfirmationError as e:
            return {"error": e.detail}

        serializer = self.get_user_serializer_class()

        data = {"token": token}
        if serializer is not None:
            data["user"] = serializer(request.user, context=self.get_context()).data
        return data

    def get_user_serializer_class(self):
        return PublicAccountDataSerializer


class LoginWithCredentialsView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginWithCredentialsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            account = Account.objects.get(email=serializer.data["email"])
            if not account.is_active:
                raise MissingMailConfirmationError()
        except ObjectDoesNotExist:
            return Response(
                data={"error": "account doesn't exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MissingMailConfirmationError as e:
            return Response(data={"error": e.detail}, status=e.status_code)
        except ValidationError as e:
            return Response(data={"error": e.detail}, status=e.status_code)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        account = serializer.validated_data

        return Response(
            {
                "account": PublicAccountDataSerializer(account, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(account)[1],
            },
            status=status.HTTP_200_OK,
        )


class RegisterAccountView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"error": str(e)}, status=e.status_code)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        account = serializer.save()

        return Response(
            {
                "account": RegisterAccountSerializer(account, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(account)[1],
            },
            status=status.HTTP_200_OK,
        )


class UpdateAccountView(GenericAPIView):
    serializer_class = UpdateAccountSerializer

    def post(self, request):
        try:
            account = Account.objects.get(pk=request.user.pk)
            if request.user != account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return Response({"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(
                {"error": "You have no permission to do this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(account, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"error": str(e)}, status=e.status_code)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestVerificationTokenView(GenericAPIView):
    def get(self, *args, **kwargs):
        verification_token = uuid4()
        try:
            account = Account.objects.get(pk=self.request.user.pk)
            if self.request.user != account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return Response({"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(
                {"error": "You have no permission to do this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        account.verification_token = verification_token
        account.save()
        return Response(
            {
                "unique_identifier": account.unique_identifier,
                "verification_token": verification_token,
            },
            status=status.HTTP_200_OK,
        )


class VerifyAccountView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"error": str(e)}, status=e.status_code)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        account = Account.objects.get(unique_identifier=serializer.data["unique_identifier"])
        public_data = PublicAccountDataSerializer(account).data

        return Response(public_data, status=status.HTTP_200_OK)

class ChangePasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, reset_token):
        serializer = self.serializer_class(data=request.data)
        print(str(reset_token))
        try:
            serializer.is_valid(raise_exception=True)
            reset_request = PasswordResetRequestModel.objects.get(token=reset_token)
            if(reset_request.is_token_valid() == False):
                return Response({'detail': 'Invalid link or expired.'}, status=status.HTTP_400_BAD_REQUEST)
            print(str(reset_request))
            print(str(reset_request.account))
            account = reset_request.account
            if serializer.is_valid():
                account.set_password(serializer.validated_data["password"])
                account.save()
                reset_request.delete()
                return Response(data={"Operation Done": "Changed password succesfully"}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid link or expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("soup", status=status.HTTP_200_OK)
        
class RequestPasswordResetView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Don't tell the user about the error, just move on.
            # Though maybe we can add a -dev flag check to report errors while not in a production environment?
            return Response(data={"Operation Done": "Soup"}, status=status.HTTP_200_OK)
        
        serializer.save()
        return Response(data={"Operation done" : "Soup"}, status=status.HTTP_200_OK)