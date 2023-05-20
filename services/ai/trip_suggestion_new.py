import json
import logging

from journey_hub.constants import ATTRACTION_TYPES
from services.ai.trip_suggestion import TripSuggestionAI as BaseAIClient
from django.conf import settings

logger = logging.getLogger(__name__)


class TripSuggestionAINew(BaseAIClient):
    PROMPT_TEMPLATE = (
        """
        I have a trip to {destination_name} for dates {start_date}-{end_date}
        My budget is {budget}{currency}
        """
        f"""
        Create a trip plan for me (places to visit, where to stay, where to eat, etc.)
        The data should be present in JSON format with such keys:

        day: day of the trip, YYYY-MM-DD
        name: title of the place to visit
        description: description of the place to visit
        duration: time needed for this place(in hours)
        price: money needed for this place(in dollars per person)
        latitude: latitude of the place
        longitude: longitude of the place
        address: address of the place
        category: one of options from: {", ".join(ATTRACTION_TYPES)})
        Please generate only json, without additional explanations.
        Start the message content with array, without additional keys
        """
    )

    def __init__(self):
        super().__init__()
        self.api_url = 'https://api.openai.com/v1/chat/completions'

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {settings.CHAT_GPT_TOKEN}'
        }

    def get_request_body(self, prompt_data: dict):
        return {
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "user",
                    "content": self.get_prompt(prompt_data)
                }]
        }

    @staticmethod
    def process_response(response: bytes):
        """
        Processes response
        :param response: ChatGPT response in format
        data: {
            "message": {
                "content": {
                    "parts": ["Some text ```{...}"]
                }
            }
        }
        data: {"message": ....}
        data: {"message": ....}
        data: [DONE]
        ...

        :return: parsed dict with trip data
        """

        response_data = json.loads(response)
        choices = response_data.get('choices')
        if not choices or len(choices) == 0:
            logger.error(f'No choices available')
            return {}

        choice = choices[0]
        message_content = choice.get('message', {}).get('content')
        return json.loads(message_content)
