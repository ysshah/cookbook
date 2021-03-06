# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0002_auto_20160924_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookbook.Recipe')),
            ],
        ),
        migrations.RenameModel(
            old_name='Instruction',
            new_name='RecipeInstruction',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
