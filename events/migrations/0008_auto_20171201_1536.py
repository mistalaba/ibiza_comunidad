# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-01 14:36
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20171201_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to='event_photos/'),
        ),
    ]
