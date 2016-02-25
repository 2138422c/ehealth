from __future__ import unicode_literals
from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    #avatar = models.ImageField()
    DOB = models.DateField('Date of Birth')
    email = models.EmailField()
    #age = date.today.year - DOB.year - ((date.today.month, date.today.day) < (DOB.month, DOB.day))
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    def __str__(self):
        return self.user_name

