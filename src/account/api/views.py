from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.api.serializers import RegisterAccountSerializer


@api_view(['POST'])
def register_account_view(request):
    serializer = RegisterAccountSerializer(data=request.data)
    data = dict()

    if serializer.is_valid():
        account = serializer.save()
        data['success'] = 'successfully registered new user.'
        data['email'] = account.email
        data['username'] = account.username
    else:
        data = serializer.errors

    return Response(data)
