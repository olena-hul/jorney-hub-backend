from django.urls import path, include
from rest_framework import routers

from .views import (
    DestinationListAPIView, SuggestTripAPIView, BudgetViewSet, BudgetEntryViewSet, TripViewSet,
)

router = routers.DefaultRouter()
router.register(r'budgets', BudgetViewSet)
router.register(r'budget-entries', BudgetEntryViewSet)
router.register(r'trips', TripViewSet)


urlpatterns = [
    path('destinations/', DestinationListAPIView.as_view(), name='destination-list'),
    path('suggest-trip/', SuggestTripAPIView.as_view(), name='suggest-trip-view'),
    path('', include(router.urls)),
]
