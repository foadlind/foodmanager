# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-25 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0010_auto_20180325_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
    ]