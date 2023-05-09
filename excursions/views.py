from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import FirebaseAuthentication
from excursions.models import Excursion, ExcursionAttraction, ExcursionBooking
from excursions.serializers import ExcursionSerializer, ExcursionUpdateSerializer, ExcursionAttractionSerializer, \
    ExcursionBookingSerializer, ExcursionBookingListSerializer
from services.payment.stripe_service import StripeClient


# Create your views here.
class ExcursionViewSet(ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [FirebaseAuthentication]

    def get_serializer_class(self):
        if self.action == 'update':
            return ExcursionUpdateSerializer
        return ExcursionSerializer

    # Override the update method to handle updates to entries
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        excursion_attractions = request.data.pop('excursion_attractions', [])

        # Update the budget instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update the budget entry instances
        for excursion_attraction in excursion_attractions:
            id_ = excursion_attraction.pop('id')
            attraction = ExcursionAttraction.objects.get(pk=id_)
            attraction_serializer = ExcursionAttractionSerializer(
                attraction, data=excursion_attraction, partial=True
            )
            attraction_serializer.is_valid(raise_exception=True)
            attraction_serializer.save()

        return Response(data=serializer.data)


class ExcursionAttractionViewSet(ModelViewSet):
    queryset = ExcursionAttraction.objects.all()
    serializer_class = ExcursionAttractionSerializer
    permission_classes = [FirebaseAuthentication]


class ExcursionBookingViewSet(ModelViewSet):
    queryset = ExcursionBooking.objects.all()
    serializer_class = ExcursionBookingSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ExcursionBookingListSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if user_id:
            self.queryset = self.queryset.filter(
                user_id=user_id
            ).order_by('-excursion__date')

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        excursion = serializer.validated_data.get('excursion')
        session_id, session_url = StripeClient().create_session(
            price=excursion.price,
            currency=excursion.currency,
            product_name=excursion.name,
            user_email=serializer.validated_data.get('user').email
        )
        serializer._validated_data = {
            **serializer.validated_data,
            'session_id': session_id,
            'session_url': session_url,
        }
        self.perform_create(serializer)
        return Response(data=serializer.data)


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session = request.data.get('data', {}).get('object')
        session_id = session.get('id')
        booking = ExcursionBooking.objects.get(session_id=session_id)
        booking.payment_status = session.get('payment_status')
        booking.save()
        return Response(data='ok', status=status.HTTP_200_OK)
