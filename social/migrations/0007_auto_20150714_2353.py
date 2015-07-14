# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_commentlike'),
    ]

    operations = [
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
    ]
