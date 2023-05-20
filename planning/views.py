import calendar
import uuid
from collections import Counter, defaultdict
from datetime import timedelta, datetime
from http import HTTPStatus

from django.db.models import Subquery, Avg
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import FirebaseAuthentication
from journey_hub.constants import BUDGET_CATEGORIES
from journey_hub.utils import get_price_in_usd
from services.image_upload.firebase import FirebaseStorageClient
from .models import Destination, Budget, BudgetEntry, Trip, Attraction, TripAttraction, CustomExpense
from .serializers import DestinationSerializer, SuggestTripSerializer, BudgetSerializer, BudgetEntrySerializer, \
    BudgetUpdateSerializer, TripSerializer, AttractionSerializer, TripAttractionSerializer, TripDetailSerializer, \
    ImageSerializer, TripAttractionCreateSerializer, CustomExpenseSerializer, CustomExpenseCreateSerializer


class DestinationListAPIView(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        top = request.query_params.get('top')
        if top:
            self.queryset = self.queryset.annotate(avg_rating=Avg('rates__value')).order_by('-avg_rating')[:int(top)]
        return super().list(request, *args, **kwargs)


class AttractionListAPIView(generics.ListAPIView):
    queryset = Attraction.objects.order_by('-views_count')
    serializer_class = AttractionSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        destination_id = request.query_params.get('destination_id')
        top = request.query_params.get('top')

        if destination_id:
            self.queryset = self.queryset.filter(destination__id=destination_id)

        if top:
            self.queryset = self.queryset.annotate(avg_rating=Avg('rates__value')).order_by('-avg_rating')[:int(top)]

        return super().list(request, *args, **kwargs)


class SuggestTripAPIView(APIView):
    serializer_class = SuggestTripSerializer
    permission_classes = [AllowAny]

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

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('mine'):
            return TripDetailSerializer

        if self.action == 'retrieve':
            return TripDetailSerializer

        return self.serializer_class

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        destination_id = request.query_params.get('destination_id')
        mine = request.query_params.get('mine')
        user = request.user
        
        if start_date and end_date and destination_id:
            self.queryset = self.queryset.filter(
                start_date=start_date,
                end_date=end_date,
                destination_id=destination_id,
                user=user,
            )

        if mine:
            self.queryset = self.queryset.filter(user=user).order_by('-created_at')
        
        return super().list(request, *args, **kwargs)

    @action(url_path='trip-days', methods=['GET'], detail=False)
    def get_trip_days(self, request, *args, **kwargs):
        user = request.user

        trips = Trip.objects.filter(user=user)

        dates = []
        for trip in trips:
            start_date = trip.start_date
            while start_date <= trip.end_date:
                dates.append(start_date)
                start_date += timedelta(days=1)

        dates_dict = Counter(date.month for date in dates)

        all_months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        results = {month: 0 for month in all_months}

        results.update({
            calendar.month_name[key]: value
            for key, value in dates_dict.items()
        })

        return Response(data=results, status=HTTPStatus.OK)

    @action(url_path='trip-expenses', methods=['GET'], detail=False)
    def get_trip_expenses(self, request, *args, **kwargs):
        user = request.user

        trip_attractions = TripAttraction.objects.filter(
            trip__user=user,
            visited=True,
        )
        custom_expenses = CustomExpense.objects.filter(
            trip__user=user
        )

        results = {category: 0 for category in BUDGET_CATEGORIES}

        for trip_attraction in trip_attractions:
            results[trip_attraction.attraction.budget_category] += float(get_price_in_usd(
                trip_attraction.price,
                trip_attraction.currency
            ))

        for custom_expense in custom_expenses:
            results[custom_expense.budget_category] += float(get_price_in_usd(
                custom_expense.price,
                custom_expense.currency
            ))

        return Response(data=results, status=HTTPStatus.OK)

    @action(url_path='visited-places', methods=['GET'], detail=False)
    def get_visited_places(self, request, *args, **kwargs):
        user = request.user
        destinations = Destination.objects.filter(
            trips__id__in=Trip.objects.filter(user=user, end_date__lt=datetime.now()).values('destination')
        )
        results = DestinationSerializer(destinations, many=True)
        return Response(data=results.data, status=HTTPStatus.OK)


class TripAttractionViewSet(ModelViewSet):
    queryset = TripAttraction.objects.all()
    serializer_class = TripAttractionSerializer
    permission_classes = [FirebaseAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return TripAttractionCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


class CustomExpenseViewSet(ModelViewSet):
    queryset = CustomExpense.objects.all()
    serializer_class = CustomExpenseSerializer
    permission_classes = [FirebaseAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomExpenseCreateSerializer
        return self.serializer_class


class ImageUploadView(APIView):
    permission_classes = [FirebaseAuthentication]

    def post(self, request):
        file = request.FILES.get('image')
        image_url = FirebaseStorageClient().upload(
            image=file,
            name=f'Attraction-{uuid.uuid4()}'
        )
        data = {
            'user': request.POST.get('user'),
            'attraction': request.POST.get('attraction'),
            'image_url': image_url,
        }
        serializer = ImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
