from django.urls import path

from .views import (
    DestinationListAPIView, SuggestTripAPIView,
)

urlpatterns = [
    path('destinations/', DestinationListAPIView.as_view(), name='destination-list'),
    path('suggest-trip/', SuggestTripAPIView.as_view(), name='suggest-trip-view')
]
