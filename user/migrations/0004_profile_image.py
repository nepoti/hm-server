# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(default=''), size=2, default=['', '']),
        ),
    ]
