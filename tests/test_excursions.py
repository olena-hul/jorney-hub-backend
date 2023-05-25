from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from authentication.models import User
from excursions.models import Excursion, ExcursionAttraction
from planning.models import Attraction, Location, Destination
from ratings.models import Rate


class ExcursionAndRatesViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(password='test', email='test@gmail.com', role_id=1)
        self.client.force_authenticate(user=self.user)
        self.patcher = patch('authentication.permissions.FirebaseAuthentication.has_permission')
        self.mock_function = self.patcher.start()
        self.mock_function.return_value = True
        self.excursion = Excursion.objects.create(
            name='Excursion 1',
            guide=self.user,
            description='Excursion description',
            date='2023-01-01',
            price=100.0,
            currency='USD',
            start_address='Excursion start address',
        )
        location = Location.objects.create(longitude=0, latitude=0)
        self.destination1 = Destination.objects.create(
            name='Destination 1',
            views_count=100,
            image_urls=[],
            description='test',
            destination_type='city',
            location=location,
        )
        self.attraction1 = Attraction.objects.create(
            **{
                "name": "Independence Square",
                "description": "Main square of Kyiv, with Independence Monument, fountains & landmarks of Kyiv's political history.",
                "duration": 2,
                "price": 0,
                "location_id": location.id,
                "address": "Maidan Nezalezhnosti, Kyiv, Ukraine",
                "budget_category": "Activities",
                "image_urls": [],
                "destination_id": self.destination1.id
            }
        )
        self.attraction2 = Attraction.objects.create(
            **{
                "name": "Independence Square 2",
                "description": "Main square of Kyiv, with Independence Monument, fountains & landmarks of Kyiv's political history.",
                "duration": 2,
                "price": 0,
                "location_id": location.id,
                "address": "Maidan Nezalezhnosti, Kyiv, Ukraine",
                "budget_category": "Activities",
                "image_urls": [],
                "destination_id": self.destination1.id
            }
        )
        self.excursion_attraction1 = ExcursionAttraction.objects.create(
            excursion=self.excursion,
            attraction=self.attraction1,
            start_time='2023-01-01 10:00:00',
            end_time='2023-01-01 12:00:00',
            description='Attraction 1 description'
        )
        self.excursion_attraction2 = ExcursionAttraction.objects.create(
            excursion=self.excursion,
            attraction=self.attraction2,
            start_time='2023-01-01 14:00:00',
            end_time='2023-01-01 16:00:00',
            description='Attraction 2 description'
        )

    def test_list_excursions(self):
        response = self.client.get(reverse('excursion-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Excursion.objects.count())

    def test_create_excursion(self):
        response = self.client.post(reverse('excursion-list'), data={
            'guide': self.user.id,
            'name': 'Excursion new',
            'description': 'Excursion description',
            'date': '2023-01-01',
            'price': 100.0,
            'currency': '$',
            'start_address': 'Excursion start address',
            "excursion_attractions": [
                {
                    "attraction": self.attraction1.name,
                    "start_time": "2022-03-03",
                    "end_time": "2022-03-03",
                    "description": "test"
                },
                {
                    "attraction": self.attraction2.name,
                    "start_time": "2022-03-03",
                    "end_time": "2022-03-03",
                    "description": "test"
                }
            ],

        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'Excursion new')

    def test_create_excursion_booking(self):
        self.patcher = patch('services.payment.stripe_service.StripeClient.create_session')
        self.mock_function = self.patcher.start()
        self.mock_function.return_value = (10, 'test_url')

        response = self.client.post(reverse('excursionbooking-list'), data={
            'user': self.user.id,
            'excursion': self.excursion.id,
            'adults_count': 2,
            'children_count': 1,
            'phone_number': '0964409751',

        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('session_url'), 'test_url')

    def test_create_rate_attraction(self):
        response = self.client.post(reverse('rate-list'), data={
            'user': self.user.id,
            'attraction': self.attraction1.id,
            'value': 2,
            'feedback': 'bad',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.first().attractions.first().id, self.attraction1.id)

    def test_create_rate_destination(self):
        response = self.client.post(reverse('rate-list'), data={
            'user': self.user.id,
            'destination': self.destination1.id,
            'value': 2,
            'feedback': 'bad',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.first().destinations.first().id, self.destination1.id)


