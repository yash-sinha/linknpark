# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-25 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_authority'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='karma_points',
            field=models.IntegerField(default=0),
        ),
    ]