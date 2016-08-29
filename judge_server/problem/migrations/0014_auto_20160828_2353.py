# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0013_auto_20160828_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='test_type',
            field=models.CharField(choices=[('normal', 'normal'), ('ignBlank', 'ignore blank'), ('ignPunct', 'ignore punctuation'), ('SPJ', 'special judge')], default='normal', max_length=8),
        ),
    ]
