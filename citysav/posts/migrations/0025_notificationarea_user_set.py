# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-09 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_auto_20170502_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationarea',
            name='user_set',
            field=models.BooleanField(default=False),
        ),
    ]
