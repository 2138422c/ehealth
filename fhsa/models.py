from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
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


    def __unicode__(self):
        return self.user.username

