# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fhsa', '0005_userfolder_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfolder',
            name='results',
        ),
    ]
