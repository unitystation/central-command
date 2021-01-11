from knox.views import LoginView
from knox.models import AuthToken
from rest_framework import status, generics
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from account.models import Account
from account.api.serializers import (
    AccountSerializer,
    UpdateAccountSerializer,
    RegisterAccountSerializer,
    UpdateCharacterSerializer,
)


class RegisterAccount(generics.GenericAPIView):
    serializer_class = RegisterAccountSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = dict()
        st = status.HTTP_400_BAD_REQUEST

        if serializer.is_valid():
            account = serializer.save()
            data["success"] = "successfully registered new user."
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = AuthToken.objects.create(account)[1]
            st = status.HTTP_201_CREATED
        else:
            data = serializer.errors

        return Response(status=st, data=data)


class Login(LoginView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        st = status.HTTP_400_BAD_REQUEST

        if serializer.is_valid():
            account = serializer.validated_data["user"]
            login(request, account)
            data = super(Login, self).post(request, format=None)
            data["success"] = "Successfully logged in"
            return data
        else:
            data = serializer.errors

        return Response(data=data, status=st)


class AccountById(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateAccountSerializer
    lookup_field = "user_id"

    def get(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(user_id=self.kwargs["user_id"])

            if not request.user.is_staff and not account == request.user:
                raise PermissionDenied

        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serialized = AccountSerializer(account)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(user_id=self.kwargs["user_id"])

            if not request.user == account:
                raise PermissionDenied
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        return Account.objects.filter(user_id=self.kwargs["user_id"])


class CharacterById(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateCharacterSerializer
    lookup_field = "user_id"

    def get(self, request, *args, **kwargs):
        try:
            character = Account.objects.get(user_id=self.kwargs["user_id"])
            if request.user != character:
                raise PermissionDenied
        except Account.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serialized = AccountSerializer(character)

        return Response(
            serialized.data.get("character_settings"), status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        try:
            character = Account.objects.get(user_id=self.kwargs["user_id"])
            if request.user != character:
                raise PermissionDenied
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.update(request, *args, **kwargs)
