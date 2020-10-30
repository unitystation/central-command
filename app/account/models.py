from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    """
    Handles all account operations, like creating and saving.
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("All accounts must have an email.")

        if not username:
            raise ValueError("All accounts must have an account name.")

        account = self.model(
            email=self.normalize_email(email),
            username=username
        )

        account.set_password(password)
        account.save(using=self._db)

        return account

    def create_staff(self, email, username, password):
        if not email:
            raise ValueError("All accounts must have an email.")

        if not username:
            raise ValueError("All accounts must have an account name.")

        account = self.model(
            email=self.normalize_email(email),
            username=username
        )
        account.set_password(password)
        account.staff = True

        account.save(using=self._db)

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError("All accounts must have an email.")

        if not username:
            raise ValueError("All accounts must have an account name.")

        account = self.model(
            email=self.normalize_email(email),
            username=username
        )
        account.set_password(password)
        account.staff = True
        account.admin = True
        account.superuser = True

        account.save(using=self._db)


class Account(AbstractBaseUser):
    """
    Represents the account object. All users have an account.
    """

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=50, unique=False)
    uid = models.CharField(verbose_name="user id", max_length=28, unique=True, primary_key=True)

    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    def __str__(self):
        return f"{self.uid} - {self.username}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.superuser
