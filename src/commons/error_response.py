from logging import getLogger

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = getLogger(__name__)


class ErrorResponse(Response):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__({"error": message}, status=status_code)


def custom_exception_handler(exc, context):
    """
    This function handles all exceptions that are not handled by DRF's default exception handler.
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
    else:
        logger.error("An unhandled error occurred: %s", exc)
        logger.error("Context: %s", context)
        return ErrorResponse(f"An unhandled error occurred: {exc}")

    return response
