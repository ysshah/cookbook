# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0010_recipeingredient_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='location',
            field=models.CharField(choices=[('pantry', 'Pantry'), ('fridge', 'Fridge'), ('freezer', 'Freezer')], default='pantry', max_length=10),
            preserve_default=False,
        ),
    ]
