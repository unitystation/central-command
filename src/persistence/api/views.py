from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..models import Other, PolyPhrase
from .serializers import OtherSerializer, PolyPhraseSerializer


class ReadOtherDataView(GenericAPIView):
    serializer_class = OtherSerializer

    def get(self, request):
        try:
            other = Other.objects.get(pk=request.user.pk)
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
        data = {"account": request.user.pk}
        data["other_data"] = request.data.get("other_data")

        try:
            if not request.user.is_authorized_server:
                raise PermissionDenied
            other = Other.objects.get(pk=request.user.pk)
        except ObjectDoesNotExist:
            serializer = self.serializer_class(data=data)
            return self.try_write_to_record(serializer)
        except PermissionDenied:
            data = {"error": "You do not have permission to edit this data!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            data = self.update_other_data_dict(data, other.other_data)
            serializer = self.serializer_class(other, data=data)
            return self.try_write_to_record(serializer)

    def update_other_data_dict(self, new_data: dict, old_data: dict) -> dict:
        final_data = {"account": new_data["account"]}
        for key, value in new_data.get("other_data").items():
            old_data[key] = value
        final_data["other_data"] = old_data
        return final_data

    def try_write_to_record(self, serializer: OtherSerializer) -> Response:
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            data = {"error": e.detail}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
