# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-20 11:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0013_imagenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selecciones',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='selecciones',
        ),
        migrations.DeleteModel(
            name='usuarios',
        ),
    ]
