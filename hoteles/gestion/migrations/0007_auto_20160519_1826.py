# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-19 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_auto_20160519_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoteles',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='hoteles',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='hoteles',
            name='email',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='hoteles',
            name='phone',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='hoteles',
            name='web',
            field=models.CharField(max_length=64),
        ),
    ]
