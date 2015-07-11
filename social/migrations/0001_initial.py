# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_migrate_existing_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('likes_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('text', models.TextField(default='', blank=True)),
                ('photos', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=None)),
                ('locations', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), size=None)),
                ('author', models.ForeignKey(related_name='posts', to='user.UserProfile')),
            ],
        ),
    ]
