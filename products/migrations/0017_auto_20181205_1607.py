# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-12-05 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20181204_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name_category',
            field=models.CharField(max_length=120),
        ),
    ]
