from firebase_admin import auth
from rest_framework import serializers

from authentication.exceptions import FirebaseException
from authentication.models import User, Role
from authentication.utils import verify_token
from journey_hub.constants import Roles


class BaseUserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='name', queryset=Role.objects.all())

    def validate(self, attrs):
        if attrs['role'].name == Roles.ADMIN:
            raise serializers.ValidationError("Can't create an admin user")
        return super().validate(attrs)


class UserRegistrationSerializerGoogleAuth(BaseUserRegistrationSerializer):
    token = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, validators=[])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'role',
            'token',
        )

    def create(self, validated_data):
        token = validated_data.pop('token')
        uid = verify_token(token)

        if not uid:
            raise FirebaseException(f'User is not verified')

        validated_data['firebase_user_id'] = uid
        user, _ = User.objects.get_or_create(**validated_data)
        return user


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    password = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'role',
        )

    def create(self, validated_data):
        try:
            firebase_user = auth.create_user(
                email=validated_data['email'],
                password=validated_data.pop('password'),
                display_name=f'{validated_data["first_name"]} {validated_data["last_name"]}'
            )
            validated_data['firebase_user_id'] = firebase_user.uid
        except Exception as e:
            raise FirebaseException(f'Error while creating user on firebase: {e}')

        try:
            auth_user = User.objects.create(**validated_data)
            return auth_user
        except Exception as e:
            auth.delete_user(uid=firebase_user.uid)
            raise Exception(f'Error while creating user: {e}')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
