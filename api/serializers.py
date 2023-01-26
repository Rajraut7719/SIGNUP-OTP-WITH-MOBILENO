from .utils import send_otp
from datetime import datetime, timedelta
import random
from django.conf import settings
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN__PASSWORD_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {settings.MIN__PASSWORD_LENGTH} character"
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN__PASSWORD_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {settings.MIN__PASSWORD_LENGTH} character"
        },
    )

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'email',
            'password1',
            'password2'
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password do not match')
        return data

    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        user = User(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY

        )
        user.set_password(validated_data['password1'])
        user.save()
        send_otp(validated_data["phone_number"], otp)
        return user
