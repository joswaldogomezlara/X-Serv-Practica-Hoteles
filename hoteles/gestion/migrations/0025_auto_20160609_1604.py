# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0024_auto_20160607_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='background_colour',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='letter_size',
            field=models.CharField(max_length=64, null=True),
        ),
    ]