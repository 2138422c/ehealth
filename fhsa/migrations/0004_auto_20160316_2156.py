# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fhsa', '0003_result_retrieved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='retrieved',
            field=models.DateField(null=True),
        ),
    ]
