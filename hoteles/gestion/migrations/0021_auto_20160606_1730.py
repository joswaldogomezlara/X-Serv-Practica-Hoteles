# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-06 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0020_selecciones_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecciones',
            name='nombre',
            field=models.CharField(default='anonimo', max_length=64),
        ),
    ]
