from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from persistence.api.serializers import PolyPhrasesSerializer
from persistence.models import PolyPhrase


@api_view(['GET'])
def poly_phrase_by_id_view(request, phrase_id):
    try:
        phrase = PolyPhrase.objects.get(phrase_id=phrase_id)
    except PolyPhrase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized = PolyPhrasesSerializer(phrase)
    return Response(serialized.data)


@api_view(['GET'])
def poly_random_phrase_view(request):
    try:
        phrase = PolyPhrase.objects.order_by('?').first()
    except Exception as e:
        error = {'error': f'{e}'}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serialized = PolyPhrasesSerializer(phrase)
    return Response(serialized.data)