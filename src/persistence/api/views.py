from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from persistence.models import PolyPhrase
from persistence.api.serializers import PolyPhrasesSerializer


@api_view(["GET"])
def poly_phrase_by_id_view(request, phrase_id):
    try:
        phrase = PolyPhrase.objects.get(phrase_id=phrase_id)
    except PolyPhrase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized = PolyPhrasesSerializer(phrase)
    return Response(serialized.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def poly_random_phrase_view(request):
    try:
        phrase = PolyPhrase.objects.order_by("?").first()
    except Exception as e:
        error = {"error": f"{e}"}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serialized = PolyPhrasesSerializer(phrase)
    return Response(serialized.data)


@api_view(["POST"])
def poly_store_phrase_view(request):
    try:
        user = request.user
        text = request.data.get("phrase")

        if not user or not text:
            raise Exception("Phrase and user saying it are required!")

        phrase = PolyPhrase.objects.create(said_by=user, phrase=text)

        phrase.save()

    except Exception as e:
        error = {"error": f"{e}"}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_200_OK)
