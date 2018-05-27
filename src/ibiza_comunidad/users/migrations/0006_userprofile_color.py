# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-07 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import ibiza_comunidad.users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171125_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='color',
            field=models.CharField(default=ibiza_comunidad.users.utils.assign_random_user_color, max_length=7),
        ),
    ]