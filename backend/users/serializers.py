from rest_framework import serializers
from .models import User
class PhoneSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number',]


class VerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()