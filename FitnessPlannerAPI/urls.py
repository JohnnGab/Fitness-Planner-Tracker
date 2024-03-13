from django.urls import path, include
from . views import ExercisesListView, WorkoutPlanViewSet, GoalViewSet, ProgressLogViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'workout-plan', WorkoutPlanViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'progress_logs', ProgressLogViewSet)

urlpatterns = [
   path('exercises/', ExercisesListView.as_view(), name='exercises-list'),
   path('', include(router.urls)),
]