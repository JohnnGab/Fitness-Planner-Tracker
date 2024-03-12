from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Exercises
from .serializers import ExercisesSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary='List all exercises',
    description='Returns a list of all exercises with their details for authenticated users.',
    responses={200: ExercisesSerializer(many=True)}
)

class ExercisesListView(ListAPIView):
    queryset = Exercises.objects.all()
    serializer_class = ExercisesSerializer
    permission_classes = [IsAuthenticated]