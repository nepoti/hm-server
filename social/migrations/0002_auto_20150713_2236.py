# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes_ids',
        ),
        migrations.AlterField(
            model_name='post',
            name='locations',
            field=django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), size=None),
        ),
        migrations.AlterField(
            model_name='post',
            name='photos',
            field=django.contrib.postgres.fields.ArrayField(max_length=10, base_field=models.URLField(), size=None),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(default='', max_length=1000, blank=True),
        ),
    ]
