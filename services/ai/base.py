import logging
import uuid

import requests
from django.conf import settings

from journey_hub.constants import ATTRACTION_TYPES

logger = logging.getLogger(__name__)


class BaseAIClient:
    PROMPT_TEMPLATE = (
        """
        I have a trip to {destination_name} for dates {start_date}-{end_date}
        My budget is {budget}$
        """
        f"""
        Create a trip plan for me (places to visit, where to stay, where to eat, etc.)
        The data should be present in JSON format with such keys:
    
        day: day of the trip, DD-MM-YY
        name: title of the place to visit
        description: description of the place to visit
        duration: time needed for this place(in hours)
        price: money needed for this place(in dollars per person)
        latitude: latitude of the place
        longitude: longitude of the place
        address: address of the place
        category: one of options from: {", ".join(ATTRACTION_TYPES)})
        Please generate only json, without additional explanations
        """
    )

    def __init__(self):
        self.api_url = 'https://chat.openai.com/backend-api/conversation'
        self.user_agent = (
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
        )
        self.authorization = settings.CHAT_GPT_AUTHORIZATION
        self.cookie = settings.CHAT_GPT_COOKIE
        self.conversation_id = ''
        self.parent_message_id = ''

    @property
    def headers(self):
        return {
            'Authorization': self.authorization,
            'User-Agent': self.user_agent,
            'Cookie': self.cookie,
        }

    def get_prompt(self, prompt_data: dict):
        pass

    def get_request_body(self, prompt_data: dict):
        return {
            "action": "next",
            "messages": [
                {
                    "id": str(uuid.uuid4()),
                    "author": {
                        "role": "user"
                    },
                    "content": {
                        "content_type": "text",
                        "parts": [
                            self.get_prompt(prompt_data)
                        ]
                    }
                }
            ],
            "conversation_id": self.conversation_id,
            "parent_message_id": self.parent_message_id,
            "model": "text-davinci-002-render-sha",
            "timezone_offset_min": -180
        }

    def request(self, prompt_data: dict):
        request_body = self.get_request_body(prompt_data)
        logger.info(f'Sending request to CHAT GPT: {request_body}')
        try:
            response = requests.post(
                url=self.api_url,
                headers=self.headers,
                json=request_body,
            )
            content = response.content

            if response.status_code != 200:
                logger.error(f'An error occurred while sending request to Chat GPT: {content}')
                return {}
        except requests.RequestException as e:
            logger.error(f'An error occurred while sending request to Chat GPT: {e}')
            return {}

        return self.process_response(content)

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

        :return: parsed dict with data
        """

        pass
