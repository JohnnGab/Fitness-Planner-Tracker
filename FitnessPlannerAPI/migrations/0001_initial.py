# Generated by Django 5.0.3 on 2024-03-10 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MuscleGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPlannerAPI.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('instructions', models.TextField()),
                ('equipment', models.ManyToManyField(through='FitnessPlannerAPI.ExerciseEquipment', to='FitnessPlannerAPI.equipment')),
                ('muscle_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPlannerAPI.musclegroups')),
            ],
        ),
        migrations.AddField(
            model_name='exerciseequipment',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPlannerAPI.exercises'),
        ),
        migrations.AlterUniqueTogether(
            name='exerciseequipment',
            unique_together={('exercise', 'equipment')},
        ),
    ]