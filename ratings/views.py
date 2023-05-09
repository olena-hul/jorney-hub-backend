from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from ratings.models import Rate
from ratings.serializers import RateSerializer


# Create your views here.
class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [AllowAny]
