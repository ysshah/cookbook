# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0004_recipe_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lifespan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(max_length=200)),
                ('room_temperature', models.PositiveSmallIntegerField()),
                ('fridge', models.PositiveSmallIntegerField()),
                ('freezer', models.PositiveSmallIntegerField()),
            ],
        ),
    ]