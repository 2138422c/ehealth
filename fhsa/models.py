from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(UserProfile, null=True)
    id = models.AutoField(primary_key=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(UserFolder, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Result(models.Model):
    """
    Results from APIs
    """
    title = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=128, null=True)
    url = models.URLField(primary_key = True)
    source = models.CharField(max_length=50, null=True)
    sentimentality = models.IntegerField(default=0)
    readability = models.IntegerField(default=0)
    sensitivity = models.IntegerField(default=0)
    retrieved = models.DateField(null=True)

    def __unicode__(self):
        return self.title
