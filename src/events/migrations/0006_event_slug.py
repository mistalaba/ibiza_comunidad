# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-16 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
