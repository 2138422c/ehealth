# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 20:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('title', models.CharField(max_length=128, null=True)),
                ('description', models.CharField(max_length=128, null=True)),
                ('url', models.URLField(primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserFolder',
            fields=[
                ('name', models.CharField(max_length=32, unique=True)),
                ('description', models.TextField(max_length=500, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='profile_images')),
                ('DOB', models.DateField()),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userfolder',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fhsa.UserProfile'),
        ),
    ]
