from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from account.models import Account
from account.api.serializers import AccountSerializer, RegisterAccountSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_account_view(request):
    serializer = RegisterAccountSerializer(data=request.data)
    data = dict()
    st = status.HTTP_400_BAD_REQUEST

    if serializer.is_valid():
        account = serializer.save()
        data["success"] = "successfully registered new user."
        data["email"] = account.email
        data["username"] = account.username
        st = status.HTTP_201_CREATED
    else:
        data = serializer.errors

    return Response(status=st, data=data)


@api_view(["GET"])
def account_by_identifiers_view(request):
    email = request.data.get("email", None)
    user_id = request.data.get("user_id", None)

    if email is None and user_id is None:
        err = {"error": "at least one identifier is required to proceed. Mail or ID."}
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


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def character_by_identifier_view(request):
    email = request.data.get("email", None)
    user_id = request.data.get("user_id", None)

    if email is None and user_id is None:
        err = {"error": "at least one identifier is required to proceed. Mail or ID."}
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
            "character": serialized.data.get("character_setting", "invalid or corrupt!")
        }
        return Response(status=status.HTTP_302_FOUND, data=data)
