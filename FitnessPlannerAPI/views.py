from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Exercises, WorkoutPlan
from .serializers import ExercisesSerializer
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

#class WorkoutPlanViewSet(viewsets.ModelViewSet):
 #   queryset = WorkoutPlan.objects.all()
  #  serializer_class = WorkoutPlanSerializer

   # def get_queryset(self):
        # Optionally, filter the queryset to only include workout plans for the authenticated user
    #    return self.queryset.filter(user=self.request.user)