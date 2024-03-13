from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Exercises, WorkoutPlan, Weekday, Goal, ProgressLog
from .serializers import ExercisesSerializer, WorkoutPlanSerializer, WorkoutDayExercises, GoalSerializer, ProgressLogSerializer
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status

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

    @extend_schema(
        description="Create a new WorkoutPlan. Define workout days and Exercises for each days. Example day = 'Moday'. Provide either repetition or duration based on exercises",
        summary="Create a WorkoutPlan"
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Customize the creation process here, for example, by setting the 'user' field
        serializer.save(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request=WorkoutPlanSerializer,
        responses={200: WorkoutPlanSerializer},
        description="Update a WorkoutPlan and its associated WorkoutDayExercises. "
                    "This endpoint allows you to update the title and goal of the WorkoutPlan, "
                    "as well as add, update, or remove exercises for specific days within the plan. "
                    "Note: Any WorkoutDayExercises instances associated with the WorkoutPlan but "
                    "not included in the update request will be removed, ensuring that the "
                    "WorkoutPlan reflects exactly the exercises specified in the update. "
                    "Additionally, any WorkoutDayExercises instances not currently associated with "
                    "the WorkoutPlan but added in the update request will be created and associated "
                    "with the WorkoutPlan, allowing for the addition of new exercises.",
        summary="Update a WorkoutPlan"
    )

    def update(self, request, *args, **kwargs):
        try:
            # Retrieve the WorkoutPlan instance to be updated using the ID provided in the URL
            workout_plan = self.get_object()
             # Initialize the WorkoutPlanSerializer with the instance and the incoming data
            serializer = self.get_serializer(workout_plan, data=request.data)
            serializer.is_valid(raise_exception=True)

            # Update the WorkoutPlan fields with validated data
            workout_plan.title = serializer.validated_data.get('title', workout_plan.title)
            workout_plan.goal = serializer.validated_data.get('goal', workout_plan.goal)
            workout_plan.save()

            # Handle the workoutdayexercises_set data
            day_plan_data = serializer.validated_data.pop('workoutdayexercises_set', [])

            keep_day_exercises_ids = []

            for day_data in day_plan_data:
                day_name = day_data.pop('day')
                exercise_id = day_data.pop('exercise_id')

                # Handle potential Weekday.DoesNotExist exception
                try:
                    weekday = Weekday.objects.get(name=day_name)
                except Weekday.DoesNotExist:
                    return Response({'detail': f'Weekday "{day_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                # Handle potential Exercises.DoesNotExist exception
                try:
                    exercise = Exercises.objects.get(id=exercise_id)
                except Exercises.DoesNotExist:
                    return Response({'detail': f'Exercise with ID "{exercise_id}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update or create the WorkoutDayExercises instance
                workout_day_exercise, created = WorkoutDayExercises.objects.update_or_create(
                workout_plan=workout_plan,
                day=weekday,
                exercise=exercise,
                defaults=day_data
                )
                
                keep_day_exercises_ids.append(workout_day_exercise.id)

            # Remove WorkoutDayExercises instances not included in the update
            WorkoutDayExercises.objects.filter(workout_plan=workout_plan).exclude(id__in=keep_day_exercises_ids).delete()

            # Finalize the response
            updated_serializer = self.get_serializer(workout_plan)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
            methods=['DELETE'],
            responses={204: None},
            description="Delete a specific WorkoutPlan. Provide ID",
            summary="Delete a WorkoutPlan"
     )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        methods=['PATCH'],
        request=WorkoutPlanSerializer,
        responses={200: WorkoutPlanSerializer},
        description="Update a WorkoutPlan and its associated WorkoutDayExercises. "
                    "This endpoint allows you to update the title and goal of the WorkoutPlan, "
                    "as well as add, update, or remove exercises for specific days within the plan. "
                    "Note: Any WorkoutDayExercises instances associated with the WorkoutPlan but "
                    "not included in the update request will be removed, ensuring that the "
                    "WorkoutPlan reflects exactly the exercises specified in the update. "
                    "Additionally, any WorkoutDayExercises instances not currently associated with "
                    "the WorkoutPlan but added in the update request will be created and associated "
                    "with the WorkoutPlan, allowing for the addition of new exercises.",
        summary="Partial update of a WorkoutPlan"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        methods=['GET'],
        responses={200: WorkoutPlanSerializer},
        description="Retrieve details of a specific WorkoutPlan. Proived ID",
        summary="Retrieve a WorkoutPlan"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        methods=['GET'],
        responses={200: WorkoutPlanSerializer(many=True)},
        description="Retrieve a list of all WorkoutPlans for authenticated user",
        summary="List all WorkoutPlans"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    @extend_schema(
            description="Create Goal. Ex. metric : 'Loose weight'",
            summary="Creat Goal"
     )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Custom logic here, e.g., automatically setting the user
        serializer.save(user=self.request.user)

    @extend_schema(
            description="Delete a specific Goal. Provide ID",
            summary="Delete a WorkoutPlan"
     )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        description="Partially update Goal",
        summary="Partial update of a Goal"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        description="Retrieve details of a specific Goal. Provide ID",
        summary="Retrieve a Goal"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        description="Retrieve a list of all Goals for authenticated user",
        summary="List all Goals"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        description="Update Goal",
        summary="Update of a Goal"
     )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class ProgressLogViewSet(viewsets.ModelViewSet):
    queryset = ProgressLog.objects.all()
    serializer_class = ProgressLogSerializer

    @extend_schema(
            description="Create Progress Log. Ex. goal = Goal.id",
            summary="Create Progress Log"
     )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        goal_id = self.request.data.get('goal')
        goal = Goal.objects.get(id=goal_id)
        serializer.save(goal=goal) 

    @extend_schema(
        description="Retrieve a list of all Progress Logs for authenticated user",
        summary="Retrieve a list of all Progress Logs"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        description="Retrieve details of a Progress Log. Provide ID",
        summary="Retrieve Progress Log"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        description="Update Rrogress Log",
        summary="Update Rrogress Log"
     )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        description="Partially update  Rrogress Log",
        summary="Partial update of a Rrogress Log"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
            description="Delete a specific Progress Log. Provide ID",
            summary="Delete Progress Log"
     )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
