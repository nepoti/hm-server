# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='text',
            field=models.CharField(default='', max_length=500, blank=True),
        ),
    ]
