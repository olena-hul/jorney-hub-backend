from rest_framework import serializers

from services.ai.trip_suggestion import TripSuggestionAI
from .models import Destination, Location


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
    destination_name = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    budget = serializers.IntegerField(required=True)

    def create(self, validated_data):
        client = TripSuggestionAI()
        response = client.request(validated_data)
        return response
