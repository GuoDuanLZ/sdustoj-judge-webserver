# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 06:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0012_merge_20160828_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialjudge',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_judge', to='judge.Environment'),
        ),
        migrations.AlterField(
            model_name='specialjudge',
            name='problem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='special_judge', serialize=False, to='problem.Problem'),
        ),
    ]