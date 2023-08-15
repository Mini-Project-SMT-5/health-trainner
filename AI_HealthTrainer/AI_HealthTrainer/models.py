from django.db import models
from django.db import connections
from django.http import HttpResponse
import pymysql
# Create your models here.
class goal(models.Model):
    idgoal = models.CharField(max_length=6)
    Start = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)
    goal = models.CharField(max_length=50)
    user = models.CharField(max_length=45)
    class Meta:
        db_table="goal"
    
