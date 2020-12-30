from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import status, generics
from django.contrib.auth import login
from rest_framework.response import Response
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
            st = status.HTTP_200_OK
            login(request, account)
            data = super(LoginView, self).post(request, format=None)
            data["success"] = "Successfully logged in"
        else:
            data = serializer.errors

        return Response(data=data, status=st)


class AccountByIdentifierView(generics.GenericAPIView):
    def get(self, request):
        email = request.data.get("email", None)
        user_id = request.data.get("user_id", None)

        if email is None and user_id is None:
            err = {
                "error": "at least one identifier is required to proceed. Mail or ID."
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=err)

        try:
            if email is None:
                account = Account.objects.get(user_id=user_id)
            else:
                account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serialized = AccountSerializer(account)
            return Response(status=status.HTTP_302_FOUND, data=serialized.data)


class CharacterByIdentifierView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.data.get("email", None)
        user_id = request.data.get("user_id", None)

        if email is None and user_id is None:
            err = {
                "error": "at least one identifier is required to proceed. Mail or ID."
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=err)

        try:
            if email is None:
                account = Account.objects.get(user_id=user_id)
            else:
                account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serialized = AccountSerializer(account)
            data = {
                "character": serialized.data.get(
                    "character_settings", "invalid or corrupt!"
                )
            }
            return Response(status=status.HTTP_302_FOUND, data=data)
