# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20161015_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='/uploads1/')),
                ('post', models.IntegerField(default=0)),
            ],
        ),
    ]
