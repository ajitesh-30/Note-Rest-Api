# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-24 11:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note_api', '0003_auto_20190223_0737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='creater',
        ),
    ]
