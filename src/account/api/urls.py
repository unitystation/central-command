from django.urls import path
from account.api.views import register_account_view

app_name = 'account'

urlpatterns = [
    path('register/', register_account_view, name='Register')
]