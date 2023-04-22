from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import AnonymousOrAuthorized
from .models import Destination
from .serializers import DestinationSerializer, SuggestTripSerializer


class DestinationListAPIView(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]


class SuggestTripAPIView(APIView):
    serializer_class = SuggestTripSerializer
    permission_classes = [AnonymousOrAuthorized]

    def post(self, request):
        data = request.data
        user = getattr(request, 'user', None)

        if user:
            data['user_id'] = user.id

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(data=response)
