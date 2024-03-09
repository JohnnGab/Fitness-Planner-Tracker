from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already used.")
        return value

    def validate_password(self, value):
        validate_password(value)  # This will raise a ValidationError if the password is not valid

        # Custom password requirements
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one numeric character.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase character.")
        allowed_symbols = set("!@#$%^&*()-_+=~`|\\[{]};:'\",<.>/?")
        if not any(char in allowed_symbols for char in value):
            raise serializers.ValidationError("The password must contain at least one symbol.")

        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        return user
