# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-12-04 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20181103_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcategory',
            old_name='name',
            new_name='name_category',
        ),
    ]
