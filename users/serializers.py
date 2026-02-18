from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
import secrets
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        password = validated_data.pop('password')
        email = validated_data.get('email')
        
        first_name = full_name.strip()
        if not first_name and email:
            first_name = email.split('@', 1)[0]

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            role='User'
        )
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'role', 'is_active')

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class AdminCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'role', 'is_active')

    def create(self, validated_data):
        email = validated_data.get('email')

        # 🔐 Generate random temporary password
        temp_password = secrets.token_urlsafe(10)

        # Ensure first_name is never empty
        first_name = validated_data.get('first_name', '').strip()
        if not first_name and email:
            first_name = email.split('@')[0]

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            role=validated_data.get('role', 'User'),
            is_active=True
        )

        user.set_password(temp_password)
        user.save()

        # 🔗 Generate reset link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        # 📧 Send email
        send_mail(
            'Set Your Password',
            f"""
Hello {user.first_name},

An account has been created for you.

Please set your password using the link below:

{reset_link}

This link will expire in 24 hours.
            """,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user
