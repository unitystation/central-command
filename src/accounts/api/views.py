import logging
import secrets

from urllib.parse import urljoin
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from drf_spectacular.utils import extend_schema
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from commons.error_response import ErrorResponse
from commons.mail_wrapper import send_email_with_template

from ..models import Account, AccountConfirmation, PasswordResetRequestModel
from .serializers import (
    ConfirmAccountSerializer,
    EmailSerializer,
    LoginWithCredentialsSerializer,
    PublicAccountDataSerializer,
    RegisterAccountSerializer,
    ResetPasswordSerializer,
    UpdateAccountSerializer,
    VerifyAccountSerializer,
)

logger = logging.getLogger(__name__)


class LoginWithTokenView(KnoxLoginView):
    """
    Login by providing a token in the header of the request, Example: 'Authorization: Token <token>'.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = None

    def post(self, request, format=None):
        if request.auth is None:
            return ErrorResponse("Invalid token", status.HTTP_401_UNAUTHORIZED)

        return super().post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        user: Account = request.user

        if not user.is_confirmed:
            return ErrorResponse(
                "You must confirm your email before attempting to login.",
                status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_user_serializer_class()

        data = {"token": token}
        if serializer is not None:
            data["user"] = serializer(request.user, context=self.get_context()).data
        return data

    def get_user_serializer_class(self):
        return PublicAccountDataSerializer


class LoginWithCredentialsView(GenericAPIView):
    """
    Login by providing email and password.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginWithCredentialsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        account: Account | None = authenticate(email=email, password=password)  # type: ignore[assignment]

        if account is None:
            return ErrorResponse(
                "Unable to login with provided credentials.",
                status.HTTP_401_UNAUTHORIZED,
            )

        if not account.is_confirmed:
            return ErrorResponse(
                "You must confirm your email before attempting to login.",
                status.HTTP_401_UNAUTHORIZED,
            )

        if not account.is_active:
            return ErrorResponse("Account is suspended.", status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "account": PublicAccountDataSerializer(account, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(account)[1],
            },
            status=status.HTTP_200_OK,
        )


class RegisterAccountView(GenericAPIView):
    """
    Register a new account.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        account = serializer.save()
        return Response(
            {
                "account": PublicAccountDataSerializer(account, context=self.get_serializer_context()).data,
            },
            status=status.HTTP_200_OK,
        )


class UpdateAccountView(GenericAPIView):
    """
    Update your account data.

    **Requires Token authentication**
    """

    serializer_class = UpdateAccountSerializer

    def post(self, request):
        try:
            account = Account.objects.get(pk=request.user.pk)
            if request.user != account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return ErrorResponse("Account does not exist.", status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return ErrorResponse("You have no permission to do this action.", status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(account, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return ErrorResponse(str(e), e.status_code)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestVerificationTokenView(APIView):
    """
    Request a new verification token to verify your account in-game.

    **Requires Token authentication**
    """

    def get(self, *args, **kwargs):
        verification_token = uuid4()

        try:
            account = Account.objects.get(pk=self.request.user.pk)
            if self.request.user != account:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return ErrorResponse("Account does not exist.", status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return ErrorResponse("You have no permission to do this action.", status.HTTP_403_FORBIDDEN)

        account.verification_token = verification_token
        account.save()
        return Response(
            {
                "unique_identifier": account.unique_identifier,
                "verification_token": verification_token,
            },
            status=status.HTTP_200_OK,
        )


class VerifyAccountView(GenericAPIView):
    """
    Given a verification token, verify the account.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(unique_identifier=serializer.validated_data["unique_identifier"])
        except Account.DoesNotExist:
            return ErrorResponse(
                "Either token or unique_identifier are invalid.",
                status.HTTP_400_BAD_REQUEST,
            )

        if account.verification_token != serializer.validated_data["verification_token"]:
            return ErrorResponse(
                "Either token or unique_identifier are invalid.",
                status.HTTP_400_BAD_REQUEST,
            )

        public_data = PublicAccountDataSerializer(account).data

        return Response(public_data, status=status.HTTP_200_OK)


@extend_schema(operation_id="accounts_reset_password_<token>_create")
class ResetPasswordView(GenericAPIView):
    """
    Given a reset token and new password, reset the account's password.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, reset_token):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = PasswordResetRequestModel.objects.get(token=reset_token)
            if not reset_token.is_token_valid():
                raise PasswordResetRequestModel.DoesNotExist
        except PasswordResetRequestModel.DoesNotExist:
            return ErrorResponse("Invalid link or expired.", status.HTTP_400_BAD_REQUEST)

        account = reset_token.account
        account.set_password(serializer.validated_data["password"])
        account.save()
        reset_token.delete()

        return Response(status=status.HTTP_200_OK)


class RequestPasswordResetView(GenericAPIView):
    """
    Request a password reset link for a given mail.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(email=serializer.validated_data["email"])
        except Account.DoesNotExist:
            logger.warning(
                "Attempted to reset password for non-existing account: %s",
                serializer.validated_data["email"],
            )
            return Response(status=status.HTTP_200_OK)

        token = secrets.token_urlsafe(32)
        PasswordResetRequestModel.objects.create(account=account, token=token)

        link = urljoin(settings.PASS_RESET_URL, token)

        send_email_with_template(
            recipient=account.email,
            subject="Reset your password",
            template="password_reset.html",
            context={"link": link},
        )

        return Response(status=status.HTTP_200_OK)


class ConfirmAccountView(GenericAPIView):
    """
    Given a confirmation token, confirm the account.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = ConfirmAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data={request.data})

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        account_confirmation = AccountConfirmation.objects.get(token=serializer.validated_data["token"])
        account = account_confirmation.account

        account.is_confirmed = True
        account_confirmation.delete()
        account.save()

        return Response(status=status.HTTP_200_OK)


class ResendAccountConfirmationView(GenericAPIView):
    """
    Resend the confirmation mail for a given account.

    **Public endpoint**
    """

    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer: EmailSerializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                logger.warning(
                    "Attempted to resend confirmation mail for non-existing account: %s",
                    email,
                )
                return Response(status=status.HTTP_200_OK)

            if account.is_confirmed:
                logger.warning(
                    "Attempted to resend confirmation mail for already confirmed account: %s",
                    email,
                )
                return Response(status=status.HTTP_200_OK)

            account.send_confirmation_mail()
            return Response(status=status.HTTP_200_OK)
        else:
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
