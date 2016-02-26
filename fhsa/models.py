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
