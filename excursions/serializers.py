from rest_framework import serializers

from authentication.serializers import UserSerializer
from planning.models import Attraction
from planning.serializers import AttractionSerializer
from .models import Excursion, ExcursionAttraction, ExcursionBooking


class ExcursionAttractionSerializer(serializers.ModelSerializer):
    attraction = serializers.SlugRelatedField(queryset=Attraction.objects.all(), slug_field='name')

    class Meta:
        model = ExcursionAttraction
        fields = ['id', 'attraction', 'start_time', 'end_time', 'description']


class ExcursionAttractionDetailSerializer(serializers.ModelSerializer):
    attraction = AttractionSerializer()

    class Meta:
        model = ExcursionAttraction
        fields = ['id', 'attraction', 'start_time', 'end_time', 'description']


class ExcursionSerializer(serializers.ModelSerializer):
    excursion_attractions = ExcursionAttractionSerializer(many=True)

    class Meta:
        model = Excursion
        fields = ['id', 'guide', 'name', 'description', 'date', 'price', 'currency', 'start_address', 'excursion_attractions']

    def create(self, validated_data):
        excursion_attractions = validated_data.pop('excursion_attractions', [])
        excursion = Excursion.objects.create(**validated_data)
        excursion_attractions_instances = [
            ExcursionAttraction(**excursion_attraction_data, excursion=excursion) for excursion_attraction_data in excursion_attractions
        ]
        ExcursionAttraction.objects.bulk_create(excursion_attractions_instances)
        return excursion


class ExcursionDetailSerializer(ExcursionSerializer):
    guide = UserSerializer()
    excursion_attractions = ExcursionAttractionDetailSerializer(many=True)


class ExcursionBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExcursionBooking
        fields = ['user', 'excursion', 'adults_count', 'children_count', 'phone_number', 'session_url', 'payment_status']


class ExcursionBookingListSerializer(ExcursionBookingSerializer):
    excursion = ExcursionDetailSerializer()


class ExcursionUpdateSerializer(serializers.ModelSerializer):
    excursion_attractions = ExcursionAttractionSerializer(many=True)

    class Meta:
        model = Excursion
        fields = ['id', 'guide', 'name', 'description', 'date', 'price', 'currency', 'start_address', 'excursion_attractions']
