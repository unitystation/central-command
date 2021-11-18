from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from ..models import PolyPhrase, Other
from .serializers import PolyPhraseSerializer, OtherSerializer
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class ReadOtherDataView(GenericAPIView):
    serializer_class = OtherSerializer

    def get(self, request):
        try:
            other = Other.objects.get(pk=request.user.pk)
            if request.user != other.account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            data = {"error": "No data for this account could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            data = {"error": "You do not have permission to view this data!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(other)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WriteOtherDataView(GenericAPIView):
    serializer_class = OtherSerializer

    def post(self, request):
        try:
            other = Other.objects.get(pk=request.user.pk)
            if request.user != other.account or not request.user.is_authorized_server:
                raise PermissionDenied
        except ObjectDoesNotExist:
            data = {"error": "No data for this account could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            data = {"error": "You do not have permission to write this data!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        data = {"account": request.user.pk}
        data["other_data"] = request.data.get("other_data")

        serializer = OtherSerializer(other, data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            data = {"error": str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateOtherDataView(GenericAPIView):
    serializer_class = OtherSerializer

    def post(self, request):
        data = {"account": request.user.pk}
        data["other_data"] = request.data.get("other_data")
        serializer = OtherSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            if not request.user.is_authorized_server:
                raise PermissionDenied
        except ValidationError as e:
            response = {"error": str(e), "data": data}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            response = {"error": str(e)}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RandomPolyPhraseView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PolyPhraseSerializer

    def get(self, request):
        try:
            if PolyPhrase.objects.count() == 0:
                raise ObjectDoesNotExist
            phrase = PolyPhrase.objects.order_by("?").first()
        except ObjectDoesNotExist:
            data = {"error": "No phrases could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(phrase)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WritePolyPhraseView(GenericAPIView):
    serializer_class = PolyPhraseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            if not request.user.is_authorized_server:
                raise PermissionDenied
        except ValidationError as e:
            data = {"error": str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            data = {"error": "You do not have permission to write this data!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)