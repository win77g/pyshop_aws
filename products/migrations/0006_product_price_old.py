# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-11-02 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimage_is_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_old',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
