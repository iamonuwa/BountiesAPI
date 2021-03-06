# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('std_bounties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='tokenLockPrice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='accepted_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='usd_price',
            field=models.FloatField(null=True),
        ),
    ]
