from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User
from planning.models import Destination, Location, Trip, Attraction, TripAttraction, CustomExpense
from ratings.models import Rate


class DestinationListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('destination-list')
        location = Location.objects.create(longitude=0, latitude=0)
        self.destination1 = Destination.objects.create(
            name='Destination 1',
            views_count=100,
            image_urls=[],
            description='test',
            destination_type='city',
            location=location,
        )
        self.destination2 = Destination.objects.create(
            name='Destination 2',
            views_count=200,
            image_urls=[],
            description='test',
            destination_type='city',
            location=location,
        )
        self.user = User.objects.create_user(password='test', email='test@gmail.com', role_id=1)

    def test_list_destinations_without_top(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Destination.objects.count())

    def test_list_destinations_with_top(self):
        top = 1
        response = self.client.get(self.url, {'top': top})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), top)

    def test_list_destinations_ordered_by_avg_rating(self):
        rate1 = Rate.objects.create(value=5, user=self.user)
        rate1.destinations.add(self.destination1)

        rate2 = Rate.objects.create(value=4, user=self.user)
        rate2.destinations.add(self.destination2)

        top = 2
        response = self.client.get(self.url, {'top': top})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), top)
        self.assertEqual(response.data[0]['name'], self.destination1.name)
        self.assertEqual(response.data[1]['name'], self.destination2.name)


class AttractionListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('attraction-list')
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
        self.user = User.objects.create_user(password='test', email='test@gmail.com', role_id=1)

    def test_list_attractions_without_top(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Attraction.objects.count())

    def test_list_attractions_with_top(self):
        top = 1
        response = self.client.get(self.url, {'top': top})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), top)

    def test_list_attractions_ordered_by_avg_rating(self):
        rate1 = Rate.objects.create(value=5, user=self.user)
        rate1.attractions.add(self.attraction1)

        rate2 = Rate.objects.create(value=4, user=self.user)
        rate2.attractions.add(self.attraction2)

        top = 2
        response = self.client.get(self.url, {'top': top})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), top)
        self.assertEqual(response.data[0]['name'], self.attraction1.name)
        self.assertEqual(response.data[1]['name'], self.attraction2.name)


class TripViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(password='test', email='test@gmail.com', role_id=1)

        self.client.force_authenticate(user=self.user)
        self.patcher = patch('authentication.permissions.FirebaseAuthentication.has_permission')
        self.mock_function = self.patcher.start()
        self.mock_function.return_value = True

        location = Location.objects.create(longitude=0, latitude=0)
        self.destination1 = Destination.objects.create(
            name='Destination 1',
            views_count=100,
            image_urls=[],
            description='test',
            destination_type='city',
            location=location,
        )
        self.trip1 = Trip.objects.create(
            user=self.user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=2),
            destination=self.destination1
        )
        self.trip2 = Trip.objects.create(
            user=self.user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=5),
            destination=self.destination1
        )

        self.attraction = Attraction.objects.create(
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

    def test_list_trips_without_filters(self):
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Trip.objects.count())

    def test_list_trips_with_filters(self):
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        destination_id = self.destination1.id

        response = self.client.get(reverse('trip-list'), {'start_date': start_date, 'end_date': end_date, 'destination_id': destination_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_my_trips(self):
        response = self.client.get(reverse('trip-list'), {'mine': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Trip.objects.filter(user=self.user).count())

    def test_get_trip_days(self):
        response = self.client.get(reverse('trip-get-trip-days'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 12)

    def test_get_trip_expenses(self):
        trip_attraction = TripAttraction.objects.create(
            trip_id=self.trip1.id,
            attraction_id=self.attraction.id,
            date=datetime.now(),
            price=19,
            visited=True,
            currency='$'
        )

        response = self.client.get(reverse('trip-get-trip-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        assert response.data.get('Activities') == trip_attraction.price

    def test_get_trip_expenses_with_custom_expenses(self):
        trip_attraction = TripAttraction.objects.create(
            trip_id=self.trip1.id,
            attraction_id=self.attraction.id,
            date=datetime.now(),
            price=19,
            visited=True,
            currency='$'
        )
        custom_expense = CustomExpense.objects.create(
            trip_id=self.trip1.id,
            attraction_id=self.attraction.id,
            date=datetime.now(),
            description='test',
            price=10,
            currency='$',
            budget_category='Shopping'
        )

        response = self.client.get(reverse('trip-get-trip-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        assert response.data.get('Activities') == trip_attraction.price
        assert response.data.get('Shopping') == custom_expense.price

    def test_get_visited_places(self):
        Trip.objects.create(
            user=self.user, start_date=datetime.now() - timedelta(days=10), end_date=datetime.now() - timedelta(days=2),
            destination=self.destination1
        )
        response = self.client.get(reverse('trip-get-visited-places'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SuggestTripTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('attraction-list')
        location = Location.objects.create(longitude=0, latitude=0)
        self.user = User.objects.create_user(password='test', email='test@gmail.com', role_id=1)
        self.destination1 = Destination.objects.create(
            name='Destination 1',
            views_count=100,
            image_urls=[],
            description='test',
            destination_type='city',
            location=location,
        )
        self.patcher = patch('authentication.permissions.FirebaseAuthentication.has_permission')
        self.mock_function = self.patcher.start()
        self.mock_function.return_value = True

    def test_suggest_trip_unauthorized(self):
        response = self.client.post(reverse('suggest-trip-view'), data={
            'destination': self.destination1.name,
            "start_date": "2022-03-03",
            "end_date": "2022-03-03",
            'budget': 1000,
            'currency': '$'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('success'), True)

    def test_suggest_trip_authorized(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('suggest-trip-view'), data={
            'destination': self.destination1.name,
            "start_date": "2022-03-03",
            "end_date": "2022-03-03",
            'budget': 1000,
            'currency': '$'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('success'), True)
        self.assertEqual(Trip.objects.count(), 1)

