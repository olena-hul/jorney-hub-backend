from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import AnonymousOrAuthorized, FirebaseAuthentication
from .models import Destination, Budget, BudgetEntry, Trip
from .serializers import DestinationSerializer, SuggestTripSerializer, BudgetSerializer, BudgetEntrySerializer, \
    BudgetUpdateSerializer, TripSerializer


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


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [FirebaseAuthentication]

    def get_serializer_class(self):
        if self.action == 'update':
            return BudgetUpdateSerializer
        return BudgetSerializer

    # Override the update method to handle updates to entries
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        entries_data = request.data.pop('entries', [])

        # Update the budget instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update the budget entry instances
        for entry_data in entries_data:
            entry_id = entry_data.pop('id')
            entry = BudgetEntry.objects.get(pk=entry_id)
            entry_serializer = BudgetEntrySerializer(entry, data=entry_data, partial=True)
            entry_serializer.is_valid(raise_exception=True)
            entry_serializer.save()

        return Response(data=serializer.data)


# ViewSet for the BudgetEntry model
class BudgetEntryViewSet(ModelViewSet):
    queryset = BudgetEntry.objects.all()
    serializer_class = BudgetEntrySerializer
    permission_classes = [FirebaseAuthentication]


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [FirebaseAuthentication]

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        destination_id = request.query_params.get('destination_id')
        user = request.user
        
        if start_date and end_date and destination_id:
            self.queryset = self.queryset.filter(
                start_date=start_date,
                end_date=end_date,
                destination_id=destination_id,
                user=user,
            )
        
        return super().list(request, *args, **kwargs)
