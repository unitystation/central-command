from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from persistence.models import PolyPhrase
from persistence.api.serializers import PolyPhrasesSerializer
import random


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
        max_id = PolyPhrase.objects.all().aggregate(max_id=Max("phrase_id"))['max_id']
        if not max_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pk = random.randint(1, max_id)
        phrase = PolyPhrase.objects.get(pk=pk)
    except Exception as e:
        error = {'error': f'{e}'}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serialized = PolyPhrasesSerializer(phrase)
    return Response(serialized.data)