from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    # Match frontend field name (full_name)
    full_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')  # Remove role as frontend doesn't send it

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        password = validated_data.pop('password')
        
        # Use email as username
        email = validated_data.get('email')
        
        # Split full_name into first_name and last_name if needed
        # For simplicity, we'll put the whole name in first_name
        first_name = full_name.strip()
        if not first_name and email:
            first_name = email.split('@', 1)[0]

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            role='User'  # Default role for new registrations
        )
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'role')