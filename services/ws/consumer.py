import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer as BaseWebsocketConsumer

logger = logging.getLogger(__name__)


class WebsocketClient(BaseWebsocketConsumer):
    async def connect(self):
        self.channel_group_name = 'events'

        # Join the group
        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info('Websocket connection established')

    async def disconnect(self, close_code):
        pass

    async def event(self, message):
        logger.info(f'Sending message: {message}')
        await self.send(json.dumps(message))
