from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=100)

class Trips(models.Model):
    user_id = models.ForeignKey(Users)
    destination = models.CharField(max_length=100)
    plan = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()

class Joins(models.Model):
    user_id = models.ForeignKey(Users)
    trip_id = models.ForeignKey(Trips)
