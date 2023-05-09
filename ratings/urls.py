from django.urls import path, include
from rest_framework import routers

from ratings.views import RateViewSet

router = routers.DefaultRouter()
router.register(r'rates', RateViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
