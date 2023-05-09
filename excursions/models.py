from django.db import models
from django.db.models import CASCADE

from authentication.models import User
from journey_hub.models import AbstractBaseModel
from planning.models import Attraction


class Excursion(AbstractBaseModel):
    guide = models.ForeignKey(User, on_delete=CASCADE, related_name='excursions')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateField()
    price = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    currency = models.CharField(max_length=3)
    start_address = models.TextField()


class ExcursionAttraction(AbstractBaseModel):
    excursion = models.ForeignKey(Excursion, on_delete=CASCADE, related_name='excursion_attractions')
    attraction = models.ForeignKey(Attraction, on_delete=CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()


class ExcursionBooking(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='excursion_bookings')
    excursion = models.ForeignKey(Excursion, on_delete=CASCADE, related_name='excursion_bookings')
    payment_status = models.CharField(max_length=255, default='new')
    session_id = models.TextField(null=True)
    session_url = models.TextField(null=True)
    adults_count = models.IntegerField(default=0)
    children_count = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=255)
