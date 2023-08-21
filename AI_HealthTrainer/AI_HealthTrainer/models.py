from django.db import models
from django.db import connections
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import now

import pymysql

    
class goal(models.Model):
    # idgoal = models.CharField(max_length=6)
    start = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)
    hour = models.PositiveIntegerField(default=0)
    minute = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        db_table="goal"

class Exercise(models.Model):
    # exercise_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)

    def _str_(self):
        return self.name

    class Meta:
        db_table="exercise"

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(default = 0)
    count = models.SmallIntegerField(("Count"))
    start_time = models.DateTimeField(("Start Time"), auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(("End Time"), auto_now=False, auto_now_add=False)
    calories = models.PositiveIntegerField(default = 0)

    class Meta:
        db_table = "Workout"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_photo = models.ImageField(default='pp.png', upload_to='dp/')
    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=False, null=False, max_length=100)
    phone = models.CharField(blank=True, null=True, max_length=14)

    joined = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class UserFitnessData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.PositiveIntegerField(blank=True, null=True)
    exercise_time = models.PositiveIntegerField(default = 0)
    used_calories = models.PositiveIntegerField(default = 0)
    accomplishment_rate = models.PositiveIntegerField(null = True, blank = True)

   # def save(self, *args, **kwargs) :
        #if self.exercise_time != 0 and self.goal is not None:
            #self.accomplishment_rate = (self.exercise_time / self.goal) * 100
        #super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
