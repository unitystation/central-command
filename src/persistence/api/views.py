import secrets
import uuid

from django.core import signing
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from accounts.models import Account
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


class GenerateForkTokenView(GenericAPIView):
    """
    Creates a new character based on the token which embeds
    the fork/server and account identifier.

    **Requires token in 'X-Character-Token' header.**
    """

    serializer_class = CharacterSerializer

    def post(self, request):
        server_id = request.data.get("fork_compatibility")

        if not server_id:
            return Response({"error": "Missing 'fork_compatibility' in request body."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # You can adjust this if your field is different
        if not hasattr(user, "unique_identifier"):
            return Response({"error": "Authenticated user lacks a unique identifier."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token_data = {
            "server_id": server_id,
            "uuid": str(user.unique_identifier),
            "nonce": secrets.token_hex(8),
        }

        token = signing.dumps(token_data)

        return Response({"token": token})



class CreateCharacterViewToken(GenericAPIView):
    """
    Creates a new character based on the token which embeds
    the fork/server and account identifier.

    **Requires token in 'X-Character-Token' header.**
    """

    serializer_class = CharacterSerializer

    def generate_token(server_id: str) -> str:
        data = {"server_id": server_id, "nonce": secrets.token_hex(8), "uuid": str(uuid.uuid4())}
        return signing.dumps(data)

    def parse_token(token: str) -> dict:
        return signing.loads(token)

    def post(self, request):
        token = request.headers.get("X-Character-Token")
        if not token:
            return Response({"error": "Missing X-Character-Token header"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = signing.loads(token)
        except signing.BadSignature:
            return Response({"error": "Invalid or tampered token"}, status=status.HTTP_400_BAD_REQUEST)

        server_id = parsed.get("server_id")
        account_uuid = parsed.get("uuid")

        if not server_id or not account_uuid:
            return Response({"error": "Token missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Look up account by UUID
        try:
            account = Account.objects.get(unique_identifier=account_uuid)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        data_with_extras = request.data.copy()
        data_with_extras["account"] = account.pk
        data_with_extras["fork_compatibility"] = server_id  # Enforce fork from token

        serializer = self.serializer_class(data=data_with_extras)
        serializer.account = account  # type: ignore

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({"error": "You do not have permission to write this data!"}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteCharacterViewToken(GenericAPIView):
    """
    Deletes a character by its ID. The character must:
    - Belong to the account identified by the token's UUID.
    - Match the fork/server ID in the token.

    **Requires 'X-Character-Token' header.**
    """

    serializer_class = CharacterSerializer

    def delete(self, request, pk):
        token = request.headers.get("X-Character-Token")
        if not token:
            return Response({"error": "Missing X-Character-Token header"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = signing.loads(token)
        except signing.BadSignature:
            return Response({"error": "Invalid or tampered token"}, status=status.HTTP_400_BAD_REQUEST)

        server_id = parsed.get("server_id")
        account_uuid = parsed.get("uuid")

        if not server_id or not account_uuid:
            return Response({"error": "Token missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Look up account
        try:
            account = Account.objects.get(unique_identifier=account_uuid)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        # Attempt to get character
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"error": "No character with this ID could be found!"}, status=status.HTTP_404_NOT_FOUND)

        # Check ownership and fork
        if character.account != account:
            return Response({"error": "You do not have permission to delete this character!"},
                            status=status.HTTP_403_FORBIDDEN)

        if character.fork_compatibility != server_id:
            return Response({"error": "This character does not match the server/fork in the token!"},
                            status=status.HTTP_403_FORBIDDEN)

        character.delete()
        return Response({"success": "Character deleted successfully!"}, status=status.HTTP_200_OK)


class GetCompatibleCharactersToken(ListAPIView):
    """
    Retrieves a list of compatible characters based on the token-provided fork and account.

    **Requires 'X-Character-Token' header.**
    """

    serializer_class = CharacterSerializer

    def get_queryset(self):
        token = self.request.headers.get("X-Character-Token")
        if not token:
            raise ValidationError({"token": "Missing X-Character-Token header"})

        try:
            parsed = signing.loads(token)
        except signing.BadSignature:
            raise ValidationError({"token": "Invalid or tampered token"})

        server_id = parsed.get("server_id")
        account_uuid = parsed.get("uuid")

        if not server_id or not account_uuid:
            raise ValidationError({"token": "Token missing required fields"})

        try:
            account = Account.objects.get(unique_identifier=account_uuid)
        except Account.DoesNotExist:
            raise ValidationError({"account": "Account not found"})

        # Only expect character_sheet_version from the query
        query_data = {
            "character_sheet_version": self.request.query_params.get("character_sheet_version")
        }

        query_serializer = CompatibleCharactersRequestSerializer(data=query_data)
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        character_sheet_version = query_serializer.validated_data["character_sheet_version"]

        queryset = Character.objects.filter(
            account=account,
            fork_compatibility=server_id,
            character_sheet_version=character_sheet_version,
        )

        return queryset

class UpdateCharacterViewToken(GenericAPIView):
    """
    Updates a character by its ID using token-based authentication.

    **Requires 'X-Character-Token' header.**
    """

    serializer_class = UpdateCharacterSerializer
    queryset = Character.objects.all()

    def update_character(self, request, pk):
        token = request.headers.get("X-Character-Token")
        if not token:
            return Response({"error": "Missing X-Character-Token header"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = signing.loads(token)
        except signing.BadSignature:
            return Response({"error": "Invalid or tampered token"}, status=status.HTTP_400_BAD_REQUEST)

        server_id = parsed.get("server_id")
        account_uuid = parsed.get("uuid")

        if not server_id or not account_uuid:
            return Response({"error": "Token missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Look up account
        try:
            account = Account.objects.get(unique_identifier=account_uuid)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        # Look up character
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"error": "No character with this ID could be found!"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the character belongs to the token-provided account
        if character.account != account:
            return Response({"error": "You do not have permission to edit this character!"},
                            status=status.HTTP_403_FORBIDDEN)

        # Check fork match
        if character.fork_compatibility != server_id:
            return Response({"error": "This character does not match the server/fork in the token!"},
                            status=status.HTTP_403_FORBIDDEN)

        # Proceed with update
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