# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shorturl',
            name='short_url',
            field=models.TextField(unique=True, verbose_name='Short url'),
        ),
    ]