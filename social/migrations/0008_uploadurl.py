# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20150714_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('models', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]