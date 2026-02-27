from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

# MODELOS SIMPLES PARA POBLAR (no se usan para migraciones, solo para inserción directa)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        managed = False
        db_table = 'teams'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'activities'

class Leaderboard(models.Model):
    user_email = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'leaderboard'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user_email = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'workouts'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Borrar datos previos
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Crear índice único en email
        db.users.create_index('email', unique=True)

        # Equipos
        teams = [
            {'name': 'Marvel'},
            {'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Usuarios
        users = [
            {'email': 'ironman@marvel.com', 'name': 'Iron Man', 'team': 'Marvel'},
            {'email': 'spiderman@marvel.com', 'name': 'Spider-Man', 'team': 'Marvel'},
            {'email': 'batman@dc.com', 'name': 'Batman', 'team': 'DC'},
            {'email': 'wonderwoman@dc.com', 'name': 'Wonder Woman', 'team': 'DC'}
        ]
        db.users.insert_many(users)

        # Actividades
        activities = [
            {'name': 'Run', 'user_email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Swim', 'user_email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Cycle', 'user_email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Yoga', 'user_email': 'wonderwoman@dc.com', 'team': 'DC'}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_email': 'ironman@marvel.com', 'team': 'Marvel', 'points': 100},
            {'user_email': 'spiderman@marvel.com', 'team': 'Marvel', 'points': 80},
            {'user_email': 'batman@dc.com', 'team': 'DC', 'points': 90},
            {'user_email': 'wonderwoman@dc.com', 'team': 'DC', 'points': 95}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Pushups', 'description': 'Do 20 pushups', 'user_email': 'ironman@marvel.com'},
            {'name': 'Situps', 'description': 'Do 30 situps', 'user_email': 'spiderman@marvel.com'},
            {'name': 'Plank', 'description': 'Hold plank for 1 min', 'user_email': 'batman@dc.com'},
            {'name': 'Squats', 'description': 'Do 40 squats', 'user_email': 'wonderwoman@dc.com'}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
