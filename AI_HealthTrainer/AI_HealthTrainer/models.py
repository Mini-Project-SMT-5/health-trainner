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


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     my_photo = models.ImageField(default='pp.png', upload_to='dp/')
#     first_name = models.CharField(blank=True, max_length=20)
#     last_name = models.CharField(blank=True, max_length=20)
#     email = models.CharField(blank=False, null=False, max_length=100)
#     phone = models.CharField(blank=True, null=True, max_length=14)

#     joined = models.DateTimeField(default=now, editable=False)

#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

# class UserFitnessData(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     goal = models.PositiveIntegerField(blank=True, null=True)
#     exercise_time = models.PositiveIntegerField(default = 0)
#     used_calories = models.PositiveIntegerField(default = 0)
#     accomplishment_rate = models.PositiveIntegerField(null = True, blank = True)

#    # def save(self, *args, **kwargs) :
#         #if self.exercise_time != 0 and self.goal is not None:
#             #self.accomplishment_rate = (self.exercise_time / self.goal) * 100
#         #super().save(*args, **kwargs)
    
#     def __str__(self):
#         return self.user.username
