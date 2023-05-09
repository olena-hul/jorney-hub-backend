from django.db import models

from journey_hub.models import AbstractBaseModel


# Create your models here.
class ChatGPTCredentials(AbstractBaseModel):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
