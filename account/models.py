from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.EmailField(verbose_name='email address', unique=True)
    username = models.CharField(verbose_name='account name', max_length=50, unique=False, blank=True)
    user_id = models.CharField(verbose_name='user id', max_length=28)
    hardware_id = models.CharField(verbose_name='hardware id', max_length=28)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username




