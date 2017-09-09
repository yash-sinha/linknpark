# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-25 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_memberactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberactivity',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberactivity',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
