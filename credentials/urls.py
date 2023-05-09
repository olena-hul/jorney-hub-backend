from django.urls import path

from credentials.views import CredentialsAPIView

urlpatterns = [
    path('', CredentialsAPIView.as_view(), name='chat-gpt-credentials-update'),
]
