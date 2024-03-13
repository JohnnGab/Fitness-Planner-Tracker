from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Exercises, WorkoutPlan
from .serializers import ExercisesSerializer, WorkoutPlanSerializer
from rest_framework import viewsets
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

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)