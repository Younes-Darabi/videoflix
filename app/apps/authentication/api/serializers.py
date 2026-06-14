from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """Validates and creates a new user account."""
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({'confirmed_password': 'Passwords do not match'})
        return attrs

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        account = CustomUser(email=self.validated_data['email'])
        account.set_password(self.validated_data['password'])
        account.is_active = False
        account.save()
        return account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Validates user credentials and returns JWT tokens."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("Account is not activated")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }