# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_migrate_existing_users'),
        ('social', '0005_auto_20150714_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(related_name='likes', to='social.PostComment')),
                ('user', models.ForeignKey(to='user.UserProfile')),
            ],
        ),
    ]
