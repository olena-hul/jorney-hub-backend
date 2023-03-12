import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from authentication.managers import CustomUserManager
from journey_hub.constants import Roles
from journey_hub.models import AbstractBaseModel


class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    firebase_user_id = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    password = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.role.name == Roles.ADMIN

    @property
    def is_superuser(self):
        return self.is_staff


class Role(AbstractBaseModel):
    name = models.CharField(max_length=255)
