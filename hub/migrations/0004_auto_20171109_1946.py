# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 03:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0003_auto_20171109_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='hastags',
            new_name='hashtags',
        ),
    ]
