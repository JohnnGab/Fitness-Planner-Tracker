import os
import django
from django.db import transaction
import csv
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitnessPlanner.settings')
django.setup()

from FitnessPlannerAPI.models import Equipment, MuscleGroups, Exercises, ExerciseEquipment

def import_equipment(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Equipment.objects.get_or_create(name=row['name'])

def import_muscle_groups(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            MuscleGroups.objects.get_or_create(name=row['name'])

def import_exercises(csv_file):
    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exercise_name = row['name']
            description = row['description']
            instructions = row['instructions']
            muscle_group_name = row['muscle_group']
            # Retrieve the muscle group from the database
            try:
                muscle_group = MuscleGroups.objects.get(name=muscle_group_name)
            except ObjectDoesNotExist:
                print(f"Muscle group {muscle_group_name} does not exist. Skipping exercise {exercise_name}.")
                continue
            # Create the exercise
            Exercises.objects.get_or_create(
                name=exercise_name,
                defaults={
                    'description': description,
                    'instructions': instructions,
                    'muscle_group': muscle_group,
                }
            )

def import_exercise_equipment(csv_file):
    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exercise_name = row['exercise']
            equipment_name = row['equipment']
            is_optional = row['is_optional'].strip().upper() == 'TRUE'
            
            # Fetch the exercise by name
            try:
                exercise = Exercises.objects.get(name=exercise_name)
            except ObjectDoesNotExist:
                print(f"Exercise '{exercise_name}' does not exist in the database.")
                #continue  # Skip this row if the exercise does not exist

            # Fetch the equipment by name
            try:
                equipment = Equipment.objects.get(name=equipment_name)
            except ObjectDoesNotExist:
                print(f"Equipment '{equipment_name}' does not exist in the database.")
                #continue  # Skip this row if the equipment does not exist

            # If both exercise and equipment exist, then create the association
            ExerciseEquipment.objects.get_or_create(
                exercise=exercise,
                equipment=equipment,
                defaults={'is_optional': is_optional}
            )

def main():
    
    import_equipment('data/Equipment.csv')
    import_muscle_groups('data/MuscleGroups.csv')
    import_exercises('data/Exercises.csv')
    import_exercise_equipment('data/ExerciseEquipment.csv')

if __name__ == '__main__':
    main()