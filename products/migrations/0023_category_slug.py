# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-12-13 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_product_categ'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Транслит'),
        ),
    ]
