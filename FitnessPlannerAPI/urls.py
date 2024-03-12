from django.urls import path
from . import views
from . views import ExercisesListView

urlpatterns = [
   path('exercises/', ExercisesListView.as_view(), name='exercises-list'),
]