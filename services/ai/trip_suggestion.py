import json
import logging

from journey_hub.constants import ATTRACTION_TYPES
from services.ai.base import BaseAIClient

logger = logging.getLogger(__name__)


class TripSuggestionAI(BaseAIClient):
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
        super().__init__()
        self.conversation_id = 'cdfa506c-791f-440f-a038-9bf86d69c3ad'
        self.parent_message_id = '6414fe5a-f88d-47e6-87cc-72b478fb7440'

    def get_prompt(self, prompt_data: dict):
        return self.PROMPT_TEMPLATE.format(
            destination_name=prompt_data.get('destination_name'),
            start_date=prompt_data.get('start_date'),
            end_date=prompt_data.get('end_date'),
            budget=prompt_data.get('budget'),
        )

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

        if response == b'':
            return {}

        # Keys of message and data items
        message_start_key = b'{"message": {"id": '
        data_key = b'data: ' + message_start_key

        # Index of data: [DONE]
        last_index_of_data = response.rfind(data_key)
        # Index of the last data: {"message": ....} that contains all info
        second_from_the_last_idx_of_data = response.rfind(message_start_key, None, last_index_of_data)

        # Get data: {"message": ....} string
        data = response[second_from_the_last_idx_of_data:last_index_of_data]
        logger.info(f'DATA: {data}')

        # Get parts
        parsed_data = json.loads(data)
        parts = parsed_data.get('message').get('content').get('parts')[0]

        logger.info(f'PARTS: {data}')

        json_start_key = '```json'
        json_end_key = '```'
        object_end_key = '},\n'

        idx_of_json_start = parts.find(json_start_key)
        idx_of_json_end = parts.rfind(json_end_key)

        if idx_of_json_start == -1:
            idx_of_json_start = parts.find(json_end_key)
            if idx_of_json_start == -1:
                idx_of_json_start = 0
            else:
                json_start_key = json_end_key

        suffix = ''
        if idx_of_json_end == -1 or idx_of_json_start == idx_of_json_end:
            idx_of_json_end = parts.rfind(object_end_key)
            suffix += '}]'

        string_to_decode = ''
        try:
            string_to_decode = parts[idx_of_json_start + len(json_start_key):idx_of_json_end] + suffix
            return json.loads(string_to_decode)
        except json.JSONDecodeError as e:
            logger.exception(f'An error occurred while decoding json: {e}. The source string was: {string_to_decode}')
            return {}
