from django.db import models
from django.db.models import CASCADE

from authentication.models import User
from journey_hub.models import AbstractBaseModel


# Create your models here.
class Rate(AbstractBaseModel):
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    feedback = models.TextField(null=True)
