# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fhsa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='readability',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='sensitivity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='sentimentality',
            field=models.IntegerField(default=0),
        ),
    ]
