# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-24 09:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='recipe',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
