from rest_framework import status


class MissingMailConfirmationError(Exception):
    """Account is trying to login without confirming their email first"""

    detail = "You must confirm your email before attempting to login."
    status_code = status.HTTP_418_IM_A_TEAPOT
