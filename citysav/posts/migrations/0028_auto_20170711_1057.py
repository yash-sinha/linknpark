# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-11 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
