from uuid import uuid4

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import status
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError

from ..models import Account
from ..exceptions import MissingMailConfirmation
from .serializers import (
    UpdateAccountSerializer,
    VerifyAccountSerializer,
    RegisterAccountSerializer,
    UpdateCharactersSerializer,
    PublicAccountDataSerializer,
    LoginWithCredentialsSerializer,
)


class PublicAccountDataView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Account.objects.all()
    serializer_class = PublicAccountDataSerializer


class LoginWithTokenView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def get_post_response_data(self, request, token, instance):
        try:
            if not request.user.is_active:
                raise MissingMailConfirmation()
        except MissingMailConfirmation as e:
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
                raise MissingMailConfirmation()
        except ObjectDoesNotExist:
            return Response(
                data={"error": "account doesn't exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MissingMailConfirmation as e:
            return Response(data={"error": e.detail}, status=e.status_code)
        except ValidationError as e:
            return Response(data={"error": e.detail}, status=e.status_code)
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        account = serializer.validated_data

        return Response(
            {
                "account": PublicAccountDataSerializer(
                    account, context=self.get_serializer_context()
                ).data,
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
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        account = serializer.save()

        return Response(
            {
                "account": RegisterAccountSerializer(
                    account, context=self.get_serializer_context()
                ).data,
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
            return Response(
                {"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
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
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCharactersView(GenericAPIView):
    serializer_class = UpdateCharactersSerializer

    def post(self, request):
        try:
            account = Account.objects.get(pk=request.user.pk)
            if request.user != account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return Response(
                {"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
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
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
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
            return Response(
                {"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied:
            return Response(
                {"error": "You have no permission to do this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        account.verification_token = verification_token
        account.save()
        return Response(
            {
                "account_identifier": account.account_identifier,
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
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        account = Account.objects.get(
            account_identifier=serializer.data["account_identifier"]
        )
        public_data = PublicAccountDataSerializer(account).data

        return Response(public_data, status=status.HTTP_200_OK)
