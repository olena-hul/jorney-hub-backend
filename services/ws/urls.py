from django.urls import path

from services.ws.consumer import WebsocketClient

websocket_urlpatterns = [
    path('ws/', WebsocketClient.as_asgi()),
]
