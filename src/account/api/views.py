from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import status, generics
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from account.models import Account
from account.api.serializers import AccountSerializer, RegisterAccountSerializer


class RegisterAccountView(generics.GenericAPIView):
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


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        st = status.HTTP_400_BAD_REQUEST

        if serializer.is_valid():
            account = serializer.validated_data["user"]
            login(request, account)
            data = super(LoginView, self).post(request, format=None)
            data["success"] = "Successfully logged in"
            return data
        else:
            data = serializer.errors

        return Response(data=data, status=st)


@api_view(["GET"])
def account_by_id_view(request, user_id):
    try:
        if not request.user.is_staff:
            raise PermissionDenied

        account = Account.objects.get(user_id=user_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except PermissionDenied:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serialized = AccountSerializer(account)

    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def character_by_id_view(request, user_id):
    try:
        character = Account.objects.get(user_id=user_id)
        if request.user != character:
            raise PermissionDenied
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except PermissionDenied:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serialized = AccountSerializer(character)

    return Response(
        serialized.data.get("character_settings"), status=status.HTTP_200_OK
    )
