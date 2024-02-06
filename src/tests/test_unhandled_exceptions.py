from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ExceptionView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        raise Exception("This is a test exception")


class CustomExceptionHandlerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_exception_handler(self):
        request = self.factory.get("/fake-url")  # The URL doesn't matter here
        response = ExceptionView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["error"], "An unhandled error occurred: This is a test exception")
        self.assertIn("error", response.data)
