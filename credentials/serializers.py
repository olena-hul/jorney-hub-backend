from rest_framework import serializers


class ChatGPTCredentialsSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    user_agent = serializers.CharField(required=False)
    cookies = serializers.CharField(required=True)
