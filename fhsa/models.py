from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class UserProfile(models.Model):
    """
    The profile for users of the site
    """
    user = models.OneToOneField(User, null=True)
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    DOB = models.DateField()
    email = models.EmailField(blank=True)
   # age = int((date.today() - DOB).days / 365.2425)
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    def __unicode__(self):
        return self.user.username

class UserFolder(models.Model):
    """
    Folders that users can create
    """
    name = models.CharField(max_length=32, null=True)
    description = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(UserProfile, null=True)
    id = models.AutoField(primary_key=True)
    

    def __unicode__(self):
        return self.name