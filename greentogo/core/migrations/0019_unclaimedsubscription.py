# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-12 02:51
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170712_0140'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnclaimedSubscription',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    )
                ),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('claimed', models.BooleanField(default=False)),
                (
                    'plan',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Plan')
                ),
            ],
        ),
    ]