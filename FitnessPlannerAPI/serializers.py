from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Equipment, MuscleGroups, Exercises, ExerciseEquipment

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

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name']

class MuscleGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroups
        fields = ['name']  

class ExerciseEquipmentSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = ExerciseEquipment
        fields = ['id', 'equipment', 'is_optional']


class ExercisesSerializer(serializers.ModelSerializer):
    muscle_group = MuscleGroupsSerializer(read_only=True)
    equipment = ExerciseEquipmentSerializer(source='exerciseequipment_set', many=True, read_only=True)

    class Meta:
        model = Exercises
        fields = ['id', 'name', 'description', 'instructions', 'muscle_group', 'equipment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        equipment_data = representation['equipment']

        # Process the equipment data to separate names and check for optionality
        equipment_names = []
        optional_names = []

        for equipment in equipment_data:
            name = equipment['equipment']['name']  # Get the equipment name
            if equipment['is_optional']:
                optional_names.append(name)
            else:
                equipment_names.append(name)

        # Combine equipment names, prioritizing required equipment
        if equipment_names and optional_names:
            representation['equipment'] = f"{', '.join(equipment_names)} and {' or '.join(optional_names)}"
        elif equipment_names:
            representation['equipment'] = ' and '.join(equipment_names)
        elif optional_names:
            representation['equipment'] = ' or '.join(optional_names)
        else:
            representation['equipment'] = 'No equipment'

        return representation