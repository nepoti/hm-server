# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_migrate_existing_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='following', to='user.UserProfile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(related_name='followers', to='user.UserProfile'),
        ),
    ]
