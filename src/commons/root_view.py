from django.core.cache import cache
from django.db import DatabaseError, connections
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class RootView(APIView):
    permission_classes = (AllowAny,)

    system_status = {
        "database": "OK",
        "cache": "OK",
    }

    def get(self, request):
        try:
            connections["default"].cursor()
        except DatabaseError:
            self.system_status["database"] = "error"

        try:
            cache.set("health_check", "ok", timeout=30)
            if cache.get("health_check") != "ok":
                raise Exception("Cache check failed")
        except Exception:
            self.system_status["cache"] = "error"

        if all(value == "OK" for value in self.system_status.values()):
            self.system_status["status"] = "All systems nominal!"
            return Response(self.system_status, status=status.HTTP_200_OK)

        self.system_status["status"] = "Some systems are down!"
        return Response(self.system_status, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
