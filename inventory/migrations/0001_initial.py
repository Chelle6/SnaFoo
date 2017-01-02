# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='snack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('optional', models.BooleanField()),
                ('purchaseLocations', models.TextField()),
                ('purchaseCount', models.IntegerField()),
                ('lastPurchaseDate', models.TextField()),
            ],
        ),
    ]
