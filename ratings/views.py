from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from ratings.models import Rate
from ratings.serializers import RateSerializer, RateCreateSerializer


# Create your views here.
class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return RateCreateSerializer
        return self.serializer_class
