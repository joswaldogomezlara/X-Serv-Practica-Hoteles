# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-19 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_auto_20160519_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoteles',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]
