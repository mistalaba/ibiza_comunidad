# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-08 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20171201_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_datetime']},
        ),
    ]