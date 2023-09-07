
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from backend.api.models import User, AvatarModel, Video
from rest_framework_simplejwt.tokens import  RefreshToken

class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    status = serializers.IntegerField(read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            data = {}
            refresh = self.get_token(user)
            data['refresh'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['access_token_expires_in'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            data['refresh_token_expires_in'] = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            data['email']= user.email
            data['status'] = user.status
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email',  'password', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}
    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = tokens
        access = tokens.access_token
        data = {
            "refresh": str(refresh),
            "access": str(access),
            "status": user.status
        }
        return data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.email_verified = True
        user.status = 1
        user.save()
        return user

class CreateCheckoutSessionSerializer(serializers.Serializer):
    price_info = serializers.ListField()

class UpdatePaymentMethodSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarModel
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"