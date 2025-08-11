from django.core import signing
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from central_command.settings import SCOPE_TOKEN_TTL

class TokenOrAccount(IsAuthenticated):
    """
    Permission class that checks if the request is using a Character Token, falling back to standard account authentication if not present or invalid.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return False

        try:
            signer = signing.TimestampSigner()
            parsed = signer.unsign_object(auth_header, max_age=SCOPE_TOKEN_TTL)  # 1 day in seconds

            request.fork_compatibility = parsed.get("fork_compatibility", None)

            if isinstance(parsed, dict) and "unique_identifier" in parsed:
                # If the token is valid, we can assume the user is authenticated
                request.user = Account.objects.get(unique_identifier=parsed["unique_identifier"])
                return True
        except (signing.SignatureExpired, signing.BadSignature):
            pass # ignore it to fall back
        
        # Fallback to standard account authentication
        return super().has_permission(request, view)