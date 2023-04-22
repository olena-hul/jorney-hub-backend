from django.db import models

from authentication.models import User
from journey_hub.constants import ATTRACTION_TYPES, BUDGET_CATEGORIES
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


class Trip(AbstractBaseModel):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')


class Attraction(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    attraction_type = models.CharField(max_length=255, choices=[(type_, type_) for type_ in ATTRACTION_TYPES])
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='attractions')
    rating = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    image_urls = models.JSONField(null=True)
    duration = models.IntegerField(default=1)
    budget_category = models.CharField(max_length=255, choices=[(category, category) for category in BUDGET_CATEGORIES])


class TripAttraction(AbstractBaseModel):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trip_attractions')
    attraction = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='trip_attractions')
    date = models.DateTimeField()
    visited = models.BooleanField(default=False)
    note = models.TextField(null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, null=True)


class SuggestionResults(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestion_results', null=True)
    prompt_data = models.JSONField()
    result_data = models.JSONField()
