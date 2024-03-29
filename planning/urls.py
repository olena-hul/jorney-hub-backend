from django.urls import path, include
from rest_framework import routers

from .views import (
    DestinationListAPIView, SuggestTripAPIView, BudgetViewSet, BudgetEntryViewSet, TripViewSet, AttractionListAPIView,
    TripAttractionViewSet, ImageUploadView, CustomExpenseViewSet,
)

router = routers.DefaultRouter()
router.register(r'budgets', BudgetViewSet)
router.register(r'budget-entries', BudgetEntryViewSet)
router.register(r'trips', TripViewSet)
router.register(r'trip-attractions', TripAttractionViewSet)
router.register(r'custom-expenses', CustomExpenseViewSet)

urlpatterns = [
    path('destinations/', DestinationListAPIView.as_view(), name='destination-list'),
    path('suggest-trip/', SuggestTripAPIView.as_view(), name='suggest-trip-view'),
    path('attractions/', AttractionListAPIView.as_view(), name='attraction-list'),
    path('image-upload/', ImageUploadView.as_view(), name='upload-image'),
    path('', include(router.urls)),
]
