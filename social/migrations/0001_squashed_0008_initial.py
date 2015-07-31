# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    replaces = [(b'social', '0001_initial'), (b'social', '0002_auto_20150713_2236'), (b'social', '0003_postlike'), (b'social', '0004_postcomment'), (b'social', '0005_auto_20150714_1525'), (b'social', '0006_commentlike'), (b'social', '0007_auto_20150714_2353'), (b'social', '0008_uploadurl')]

    dependencies = [
        ('user', '0002_migrate_existing_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='', max_length=1000, blank=True)),
                ('photos', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=models.URLField(), size=None)),
                ('locations', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), size=None)),
                ('author', models.ForeignKey(related_name='posts', to='user.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(related_name='likes', to='social.Post')),
                ('user', models.ForeignKey(to='user.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='', max_length=500, blank=True)),
                ('photos', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=models.URLField(), size=None)),
                ('locations', django.contrib.postgres.fields.ArrayField(max_length=10, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), size=None)),
                ('author', models.ForeignKey(to='user.UserProfile')),
                ('post', models.ForeignKey(related_name='comments', to='social.Post')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(related_name='likes', to='social.PostComment')),
                ('user', models.ForeignKey(to='user.UserProfile')),
            ],
        ),
        migrations.AlterModelOptions(
            name='commentlike',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='postlike',
            options={'ordering': ['timestamp']},
        ),
        migrations.AddField(
            model_name='commentlike',
            name='timestamp',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postlike',
            name='timestamp',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UploadUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
