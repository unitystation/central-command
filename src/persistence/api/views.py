from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from ..models import Character
from .serializers import (
    CharacterSerializer,
    CompatibleCharactersRequestSerializer,
    UpdateCharacterSerializer,
)


class GetCharacterByIdView(GenericAPIView):
    """
    Retrieves a character by its ID. The character must belong to the account of the user.

    **Requires Token Authentication.**
    """

    serializer_class = CharacterSerializer

    def get_queryset(self):
        return Character.objects.filter(account__unique_identifier=self.request.user.unique_identifier)  # type: ignore

    def get(self, request, pk):
        try:
            character = Character.objects.get(pk=pk)
        except ObjectDoesNotExist:
            data = {"error": "No character with this ID could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            data = {"error": "You do not have permission to view this character!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCompatibleCharacters(ListAPIView):
    """
    Retrieves a list of compatible characters for the user's account.

    **Requires Token Authentication.**
    """

    serializer_class = CharacterSerializer

    def get_queryset(self):
        """
        Retrieves a list of compatible characters.

        Query Parameters:
        - fork_compatibility: The fork compatibility string.
        - character_sheet_version: The version string of the character sheet.

        Example usage:
        /api/characters/fork_compatibility=Unitystation&character_sheet_version=1.0.0
        """
        query_serializer = CompatibleCharactersRequestSerializer(data=self.request.query_params)
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        fork_compatibility = query_serializer.validated_data["fork_compatibility"]
        character_sheet_version = query_serializer.validated_data["character_sheet_version"]

        queryset = Character.objects.filter(
            account__unique_identifier=self.request.user.pk,
            fork_compatibility=fork_compatibility,
            character_sheet_version=character_sheet_version,
        )

        return queryset


class GetAllCharactersByAccountView(ListAPIView):
    """
    Retrieves a list of all characters of an account, disregarding compatibility.

    **Requires Token Authentication.**
    """

    serializer_class = CharacterSerializer

    def get_queryset(self):
        """
        Retrieves a list of all characters of an account.
        """
        unique_identifier = self.request.user.pk
        queryset = Character.objects.filter(account__unique_identifier=unique_identifier)
        return queryset


class UpdateCharacterView(GenericAPIView):
    """
    Updates a character by its ID. The character must belong to the account of the user.

    **Requires Token Authentication.**
    """

    serializer_class = UpdateCharacterSerializer
    queryset = Character.objects.all()

    def update_character(self, request, pk):
        try:
            character = Character.objects.get(pk=pk)
            if character.account != request.user:
                raise PermissionDenied

        except ObjectDoesNotExist:
            data = {"error": "No character with this ID could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            data = {"error": "You do not have permission to edit this character!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(character, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.update_character(request, pk)

    def put(self, request, pk):
        return self.update_character(request, pk)


class DeleteCharacterView(GenericAPIView):
    """
    Deletes a character by its ID. The character must belong to the account of the user.

    **Requires Token Authentication.**
    """

    serializer_class = CharacterSerializer

    def delete(self, request, pk):
        try:
            character = Character.objects.get(pk=pk)
            if character.account != request.user:
                raise PermissionDenied

        except ObjectDoesNotExist:
            data = {"error": "No character with this ID could be found!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            data = {"error": "You do not have permission to delete this character!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        character.delete()
        data = {"success": "Character deleted successfully!"}
        return Response(data, status=status.HTTP_200_OK)


class CreateCharacterView(GenericAPIView):
    """
    Creates a new character.

    **Requires Token Authentication.**
    """

    serializer_class = CharacterSerializer

    def post(self, request):
        data_with_account = request.data.copy()
        data_with_account["account"] = request.user.pk

        serializer = self.serializer_class(data=data_with_account)
        serializer.account = request.user  # type: ignore
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            data = {"error": str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            data = {"error": "You do not have permission to write this data!"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
