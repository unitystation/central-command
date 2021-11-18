from django.core.exceptions import PermissionDenied
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from ..models import Account
from .serializers import (
    PublicAccountDataSerializer,
    RegisterAccountSerializer,
    LoginWithCredentialsSerializer,
    UpdateAccountSerializer,
    UpdateCharactersSerializer
)


class PublicAccountDataView(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = PublicAccountDataSerializer


class LoginWithTokenView(KnoxLoginView):
    permission_classes = (AllowAny,)
    def get_post_response_data(self, request, token, instance):
        serializer = self.get_user_serializer_class()

        data = {
            'token': token
        }
        if serializer is not None:
            data["user"] = serializer(
                request.user,
                context=self.get_context()
            ).data
        return data

    def get_user_serializer_class(self):
        return PublicAccountDataSerializer


class LoginWithCredentialsView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginWithCredentialsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                data={'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        account = serializer.validated_data

        return Response({
            "account": PublicAccountDataSerializer(account, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(account)[1]
        }, status=status.HTTP_200_OK)


class RegisterAccountView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                data={'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        account = serializer.save()

        return Response({
            "account": RegisterAccountSerializer(account, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(account)[1],
        }, status=status.HTTP_200_OK)


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
            return Response({"error": "You have no permission to do this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(account, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                data={'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
            return Response({"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"error": "You have no permission to do this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(account, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                data={'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
