from django.db import models
from django.db import connections
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import now
import pymysql
# Create your models here.
class Goal(models.Model):
    start = models.DateField()
    stop = models.DateField()
    hour = models.CharField(max_length=50, default=0) 
    minute = models.CharField(max_length=50, default=0) 
    goal = models.CharField(max_length=50, default=0) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    class Meta:
        db_table="goal"
    
class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default='null')
    
    def _str_(self):
        return self.name
    
    class Meta:
        db_table="exercise"
        
class Workout(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, default="") 
    count = models.SmallIntegerField(("Count"))
    start_time = models.DateTimeField(("Start Time"), auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(("End Time"), auto_now=False, auto_now_add=False)
    
    class Meta:
        db_table = "Workout"


