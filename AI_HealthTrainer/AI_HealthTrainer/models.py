from django.db import models
from django.db import connections
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import now

import pymysql

class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True, default=None)
    email = models.CharField(max_length=45, null=True, default=None)
    password = models.CharField(max_length=255, null=True, default=None)
    role = models.CharField(max_length=45, null=True, default=None)

    class Meta:
        db_table = 'user'



class Goal(models.Model):
    idgoal = models.AutoField(primary_key=True)
    start = models.DateField(null=True, default=None)
    end = models.DateField(null=True, default=None)
    goal = models.IntegerField(null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'goal'


class Exercise(models.Model):
    idExercise = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True, default=None)

    class Meta:
        db_table = 'exercise'

    def _str_(self):
        return self.name

    class Meta:
        db_table="exercise"


class Workout(models.Model):
    idworkout = models.AutoField(primary_key=True)
    count = models.IntegerField(null=True, default=None)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    reps = models.IntegerField(null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Exercise_idExercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    calories = models.IntegerField(null=True, default=None)
    workout_time = models.FloatField(null=True, default=None)

    class Meta:
        db_table = 'workout'