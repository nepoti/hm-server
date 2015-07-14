# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_migrate_existing_users'),
        ('social', '0003_postlike'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='', max_length=1000, blank=True)),
                ('photos', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=models.URLField(), size=None)),
                ('locations', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), size=None)),
                ('author', models.ForeignKey(to='user.UserProfile')),
                ('post', models.ForeignKey(related_name='comments', to='social.Post')),
            ],
        ),
    ]
