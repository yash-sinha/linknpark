# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-01 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_auto_20170501_1055'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PushNotificationDetails',
        ),
    ]