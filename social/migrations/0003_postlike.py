# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_migrate_existing_users'),
        ('social', '0002_auto_20150713_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(related_name='likes', to='social.Post')),
                ('user', models.ForeignKey(to='user.UserProfile')),
            ],
        ),
    ]
