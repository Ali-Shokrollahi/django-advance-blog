from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models

from apps.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_staff=True,
            email_verified=True,
            password=password
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
        Custom user model that inherits django AbstractBaseUser
    """
    email = models.EmailField(verbose_name="email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # Verify if the user's email has been verified.
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
