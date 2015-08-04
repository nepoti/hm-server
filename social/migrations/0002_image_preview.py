# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_squashed_0008_uploadurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photos',
            field=django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=2), size=None),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='photos',
            field=django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=2), size=None),
        ),
    ]
