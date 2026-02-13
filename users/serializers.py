from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)  # matches frontend
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'role')  # include role if sent from frontend

    def create(self, validated_data):
        name = validated_data.pop('name')  # get full name from frontend
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'User')  # default to 'User' if not provided

        # Use email as username
        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=name,
            role=role
        )
        user.set_password(password)
        user.save()
        return user
