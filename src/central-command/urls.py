"""central-command URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django_email_verification import urls as mail_urls

urlpatterns = [
    # path(r'', admin.site.urls),
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("email/", include(mail_urls)),
    # API REST FRAMEWORK
    path("api/accounts/", include("accounts.api.urls", "Accounts API")),
    path("api/persistence/", include("persistence.api.urls")),
]
