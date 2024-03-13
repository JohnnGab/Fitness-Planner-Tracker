from django.urls import path, include
from . views import ExercisesListView, WorkoutPlanViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'workout-plan', WorkoutPlanViewSet)

urlpatterns = [
   path('exercises/', ExercisesListView.as_view(), name='exercises-list'),
   path('', include(router.urls)),
]