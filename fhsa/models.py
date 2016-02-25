from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    avatar = models.ImageField(null=True)
    DOB = models.DateField(null=True)
    email = models.EmailField(null=True)
    #age = date.today.year - DOB.year - ((date.today.month, date.today.day) < (DOB.month, DOB.day))
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS, null=True)


    def __unicode__(self):
        return self.user.username
