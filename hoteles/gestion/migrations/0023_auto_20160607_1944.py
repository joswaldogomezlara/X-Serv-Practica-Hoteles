# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-07 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0022_auto_20160607_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoteles',
            name='categoria',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='hoteles',
            name='estrellas',
            field=models.IntegerField(null=True),
        ),
    ]
