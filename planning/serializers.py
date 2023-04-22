from rest_framework import serializers

from tasks.trip_suggestion import suggest_trip_task
from .models import Destination, Location, Trip


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']


class DestinationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    def get_fields(self):
        fields = super(DestinationSerializer, self).get_fields()
        fields['parent_destination'] = DestinationSerializer(read_only=True, allow_null=True)
        return fields

    class Meta:
        model = Destination
        fields = '__all__'


class SuggestTripSerializer(serializers.Serializer):
    destination = serializers.SlugRelatedField(slug_field='name', queryset=Destination.objects.all(), required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    budget = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        if self.user:
            trip = Trip.objects.get_or_create(
                user=self.user,
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
