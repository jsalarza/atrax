# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20171007_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='literature',
            name='lit_desc',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='literature',
            name='lit_title',
            field=models.CharField(max_length=250),
        ),
    ]
