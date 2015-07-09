# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('user', 'UserProfile')
    for user in User.objects.all():
        user_profile = UserProfile(user=user, name=user.username)
        user_profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_profiles),
    ]
