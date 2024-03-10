from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MuscleGroups(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Exercises(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    muscle_group = models.ForeignKey(MuscleGroups, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment, through='ExerciseEquipment')

    def __str__(self):
        return self.name

class ExerciseEquipment(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = (('exercise', 'equipment'),)
