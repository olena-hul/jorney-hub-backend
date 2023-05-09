from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from planning.models import Destination, Attraction
from ratings.models import Rate


class RateSerializer(serializers.ModelSerializer):
    destination = serializers.SlugRelatedField(queryset=Destination.objects.all(), slug_field='id', required=False)
    attraction = serializers.SlugRelatedField(queryset=Attraction.objects.all(), slug_field='id', required=False)

    class Meta:
        model = Rate
        fields = ['value', 'feedback', 'user', 'destination', 'attraction']

    def validate(self, attrs):
        if (
                (not attrs.get('destination') and not attrs.get('attraction')) or
                (attrs.get('destination') and attrs.get('attraction'))
        ):
            raise ValidationError(detail='Only destination or attraction can be present')

        return attrs

    def create(self, validated_data):
        destination = validated_data.pop('destination', None)
        attraction = validated_data.pop('attraction', None)

        rate = Rate.objects.create(**validated_data)
        if destination:
            rate.destinations.add(destination)
        if attraction:
            rate.attractions.add(attraction)
        rate.save()
        return rate
