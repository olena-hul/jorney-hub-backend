from django.urls import path, include
from rest_framework import routers

from excursions.views import ExcursionViewSet, ExcursionAttractionViewSet, ExcursionBookingViewSet, StripeWebhookView

router = routers.DefaultRouter()
router.register(r'excursions', ExcursionViewSet)
router.register(r'excursion-attractions', ExcursionAttractionViewSet)
router.register(r'excursion-bookings', ExcursionBookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('stripe-webhook/', StripeWebhookView.as_view()),
]
