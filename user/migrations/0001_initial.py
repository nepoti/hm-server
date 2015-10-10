# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=30)),
                ('gender', models.CharField(default='', max_length=20, blank=True)),
                ('country', models.CharField(default='', max_length=50, blank=True)),
                ('city', models.CharField(default='', max_length=200, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('height', models.FloatField(default=0, blank=True)),
                ('weight', models.FloatField(default=0, blank=True)),
                ('blood', models.IntegerField(default=0, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
