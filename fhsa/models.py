from __future__ import unicode_literals
from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField()
    DOB = models.DateField()
    email = models.EmailField()
    #age = date.today.year - DOB.year - ((date.today.month, date.today.day) < (DOB.month, DOB.day))
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

class Query(models.Model):
    user_query = models.CharField(max_length=128)
