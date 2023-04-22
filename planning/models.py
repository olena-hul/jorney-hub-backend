from django.db import models

from journey_hub.models import AbstractBaseModel


class Location(AbstractBaseModel):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Destination(AbstractBaseModel):
    class DestinationType(models.TextChoices):
        CITY = 'city', 'City'
        COUNTRY = 'country', 'Country'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    destination_type = models.CharField(max_length=255, choices=DestinationType.choices)
    parent_destination = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destinations')
    rating = models.FloatField()
    ratings_count = models.IntegerField()
    views_count = models.IntegerField()
    image_urls = models.JSONField()
