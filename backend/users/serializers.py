from rest_framework import serializers
from .models import User, UserStripe
class PhoneSignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)


class VerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OnboardingSerializer(serializers.ModelSerializer):
    make = serializers.CharField(max_length=255)
    model = serializers.CharField(max_length=255)
    

class UserStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStripe
        fields = '__all__'