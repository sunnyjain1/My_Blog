# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-23 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160123_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='slug',
            field=models.SlugField(default='anonymous', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]