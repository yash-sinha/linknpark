# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-21 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_picture',
            field=models.TextField(blank=True),
        ),
    ]