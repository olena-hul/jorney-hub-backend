from http import HTTPStatus

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from journey_hub.utils import ApiResponse
from .serializers import (
    UserRegistrationSerializer,
    UserRegistrationSerializerGoogleAuth,
    UserSerializer, BaseUserRegistrationSerializer,
)


class AuthUserRegistrationView(APIView):
    serializer_classes = {
        'google_auth': UserRegistrationSerializerGoogleAuth,
        'password_auth': UserRegistrationSerializer,
    }
    permission_classes = (AllowAny, )

    def get_serializer_class(self, data) -> BaseUserRegistrationSerializer:
        password = data.get('password')

        if password:
            serializer_class = self.serializer_classes['password_auth']
        else:
            serializer_class = self.serializer_classes['google_auth']

        return serializer_class(data=data)

    def post(self, request):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return ApiResponse(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return ApiResponse(error=e, status=HTTPStatus.BAD_REQUEST, exception=True)


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)

    def put(self, request: Request):
        serializer = self.serializer_class(request.user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

