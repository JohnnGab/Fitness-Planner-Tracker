from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class MuscleGroups(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Exercises(models.Model):
    name = models.CharField(max_length=255, unique=True)
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

class Weekday(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'title')  # Adding unique constraint

    def __str__(self):
        return self.title
    
class WorkoutDayExercises(models.Model):
    day = models.ForeignKey(Weekday, on_delete=models.CASCADE, null=True)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    sets = models.IntegerField(help_text='Number of sets')
    repetitions = models.IntegerField(null=True, blank=True, help_text='Number of repetitions')
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in seconds')

    class Meta:
        unique_together = ('day', 'workout_plan', 'exercise')  # Adding unique constraint

    def clean(self):
        if self.repetitions is None and self.duration is None:
            raise ValidationError('Either repetitions or duration must be provided.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name}"
    
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metric = models.CharField(max_length=100, help_text="Running Distance")
    target_value = models.IntegerField(help_text="Target value for the metric")
    target_date = models.DateField()

    class Meta:
        unique_together = ('user', 'metric', 'target_date')

    def __str__(self):
        return self.type

class ProgressLog(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    date = models.DateField()
    current_value = models.IntegerField(help_text="Current value for the metric")

    class Meta:
        unique_together = ('goal', 'current_value')

    def __str__(self):
        return f"{self.goal.type} - {self.date}"