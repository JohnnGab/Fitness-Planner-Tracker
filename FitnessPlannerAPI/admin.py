from django.contrib import admin
from . models import Exercises, Equipment, MuscleGroups, ExerciseEquipment

admin.site.register(Exercises)
admin.site.register(Equipment)
admin.site.register(MuscleGroups)
admin.site.register(ExerciseEquipment)