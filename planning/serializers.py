from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ratings.serializers import RateSerializer
from tasks.trip_suggestion import suggest_trip_task
from .models import Destination, Location, Trip, BudgetEntry, Budget, Attraction, TripAttraction, CustomImage, \
    CustomExpense


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']


class DestinationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()

    def get_fields(self):
        fields = super(DestinationSerializer, self).get_fields()
        fields['parent_destination'] = DestinationSerializer(read_only=True, allow_null=True)
        return fields

    class Meta:
        model = Destination
        exclude = ['rates']


class CustomImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['image_url']
        model = CustomImage


class AttractionSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()
    custom_images = CustomImageSerializer(many=True)
    rates = RateSerializer(many=True)

    class Meta:
        model = Attraction
        fields = '__all__'


class TripAttractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripAttraction
        fields = '__all__'


class TripAttractionSerializer(serializers.ModelSerializer):
    attraction = AttractionSerializer()

    class Meta:
        model = TripAttraction
        fields = '__all__'


class SuggestTripSerializer(serializers.Serializer):
    destination = serializers.SlugRelatedField(slug_field='name', queryset=Destination.objects.all(), required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    budget = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('data', {}).pop('user', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        if self.user:
            trip, _ = Trip.objects.get_or_create(
                user=self.user,
                destination=validated_data.get('destination'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
            validated_data['trip_id'] = trip.id

        destination = validated_data.pop('destination')
        suggest_trip_task.apply_async(
            kwargs={
                'prompt_data': {
                    **validated_data,
                    'destination_id': destination.id,
                    'destination_name': destination.name,
                }
            }
        )

        return {
            "success": True
        }


class BudgetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetEntry
        fields = ('id', 'estimated_amount', 'amount_spent', 'category')


class BudgetSerializer(serializers.ModelSerializer):
    entries = BudgetEntrySerializer(many=True, required=True)

    class Meta:
        model = Budget
        fields = ('id', 'amount', 'currency', 'trip', 'entries')

    def create(self, validated_data):
        entries = validated_data.pop('entries', [])
        budget = Budget.objects.create(**validated_data)
        entries_instances = [
            BudgetEntry(**entry_data, budget=budget) for entry_data in entries
        ]
        BudgetEntry.objects.bulk_create(entries_instances)
        return budget


class BudgetUpdateSerializer(serializers.ModelSerializer):
    entries = BudgetEntrySerializer(many=True)

    class Meta:
        model = Budget
        fields = ('id', 'amount', 'currency', 'trip', 'entries')


class TripSerializer(serializers.ModelSerializer):
    budgets = BudgetSerializer(read_only=True, many=True)

    class Meta:
        model = Trip
        fields = ('id', 'start_date', 'end_date', 'budgets', 'destination', 'user')


class CustomExpenseSerializer(serializers.ModelSerializer):
    attraction = AttractionSerializer()

    class Meta:
        model = CustomExpense
        fields = ('id', 'date', 'description', 'trip', 'attraction', 'price', 'currency', 'budget_category')


class CustomExpenseCreateSerializer(serializers.ModelSerializer):
    attraction = serializers.SlugRelatedField(queryset=Attraction.objects.all(), slug_field='name')

    class Meta:
        model = CustomExpense
        fields = ('date', 'description', 'trip', 'attraction', 'price', 'currency', 'budget_category')


class ImageSerializer(ModelSerializer):
    class Meta:
        model = CustomImage
        fields = '__all__'


class TripDetailSerializer(TripSerializer):
    trip_attractions = TripAttractionSerializer(many=True)
    custom_expenses = CustomExpenseSerializer(many=True)
    destination = DestinationSerializer()

    class Meta:
        model = Trip
        fields = TripSerializer.Meta.fields + ('trip_attractions', 'custom_expenses')
