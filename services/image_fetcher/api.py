import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class ImageFetcherAPI:
    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.api_url = 'https://api.pexels.com/v1/'
        self.search_url = f'{self.api_url}search'
        self.photos_per_page = 5

    def fetch(self, attraction_name: str):
        return self.request(
            url=self.search_url,
            query_params={
                'query': attraction_name,
                'per_page': self.photos_per_page,
            }
        )

    def request(self, url: str, query_params: dict):
        logger.info(f'Sending request to PEXELS: {query_params}')
        try:
            response = requests.get(
                url=url,
                headers={
                    'Authorization': self.api_key,
                },
                params=query_params,
            )
            response_data = response.json()

            if response.status_code != 200:
                logger.error(f'An error occurred while sending request to PEXELS: {response_data}')
                return []
        except requests.RequestException as e:
            logger.error(f'An error occurred while sending request to PEXELS: {e}')
            return []

        return self.process_response(response_data)

    @classmethod
    def process_response(cls, response_data: dict):
        logger.info(f'Fetched images: {response_data}')
        photos = response_data.get('photos')
        return [
            photo.get('src', {}).get('medium') for photo in photos
        ]
