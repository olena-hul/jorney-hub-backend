import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from celery_worker import app
from journey_hub.constants import ATTRACTION_TYPE_CATEGORY_MAPPING
from planning.models import SuggestionResults, Attraction, Location
from services.ai.trip_suggestion import TripSuggestionAI
from services.image_fetcher.api import ImageFetcherAPI
from services.ws.consumer import WebsocketClient

logger = logging.getLogger(__name__)


def send_message_to_ws(data: dict | list):
    client = WebsocketClient()
    channel_layer = get_channel_layer()
    client.channel_layer = channel_layer

    async_to_sync(channel_layer.group_send)('events', {'type': 'event', 'data': data})


def process_generated_attraction(generated_attraction: dict, prompt_data: dict):
    """
    Example prompt data
    {
        "destination_id": 1
        "destination_name": "Kyiv",
        "start_date": "2023-04-19",
        "end_date": "2023-04-21",
        "budget": "500"
    }

    Example generated attraction {
        "day": "19-04-23",
        "name": "Independence Square",
        "description": "Main square of Kyiv, with Independence Monument, fountains & landmarks of Kyiv's political history.",
        "duration": 2,
        "price": 0,
        "latitude": 50.4501,
        "longitude": 30.5241,
        "address": "Maidan Nezalezhnosti, Kyiv, Ukraine",
        "category": "Historic Site"
    }
    """

    location, _ = Location.objects.get_or_create(
        latitude=generated_attraction.get('latitude'),
        longitude=generated_attraction.get('longitude'),
    )

    attraction, _ = Attraction.objects.get_or_create(
        name=generated_attraction.get('name'),
        defaults={
            'description': generated_attraction.get('description'),
            'attraction_type': generated_attraction.get('category'),
            'destination_id': prompt_data.get('destination_id'),
            'location': location,
            'address': generated_attraction.get('address'),
            'duration': generated_attraction.get('duration'),
            'budget_category': ATTRACTION_TYPE_CATEGORY_MAPPING.get(generated_attraction.get('category'))
        }
    )

    if not attraction.image_urls:
        fetch_attraction_photos.apply_async(
            kwargs={
                'attraction_id': attraction.id
            }
        )

    response_body = {
        **generated_attraction,
        'attraction_id': attraction.id,
    }

    return response_body


@app.task(name='suggest_trip_task', bind=True)
def suggest_trip_task(_, prompt_data: dict):
    trip_suggestion = TripSuggestionAI()
    result = trip_suggestion.request(prompt_data)

    if not result:
        send_message_to_ws({'error': 'Error while suggesting trip. Try again'})
        logger.error('No suggestion result')
        return

    SuggestionResults.objects.create(
        prompt_data=prompt_data,
        result_data=result,
        user_id=prompt_data.get('user_id')
    )

    response = [
        process_generated_attraction(generated_attraction, prompt_data) for generated_attraction in result
    ]

    send_message_to_ws(response)
    return response


@app.task(name='fetch_attraction_photos', bind=True)
def fetch_attraction_photos(_, attraction_id: int):
    attraction = Attraction.objects.get(id=attraction_id)
    image_fetcher = ImageFetcherAPI()
    images = image_fetcher.fetch(attraction.name)

    if images:
        attraction.image_urls = images
        attraction.save()
