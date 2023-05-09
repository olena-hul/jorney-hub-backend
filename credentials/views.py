from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatGPTCredentials
from .serializers import ChatGPTCredentialsSerializer


class CredentialsAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def create_or_update_credentials(key, value):
        credentials, created = ChatGPTCredentials.objects.get_or_create(key=key)
        if created:
            return

        credentials.value = value
        credentials.save()

    def post(self, request):
        serializer = ChatGPTCredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.data.items():
            self.create_or_update_credentials(key, value)

        return Response(
            data={'message': 'Credentials were updated successfully'},
            status=status.HTTP_200_OK
        )
