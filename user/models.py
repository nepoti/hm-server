from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=30)
    profile_image = models.URLField(blank=True, default=u'')
    gender = models.CharField(blank=True, default=u'', max_length=20)
    country = models.CharField(blank=True, default=u'', max_length=50)
    city = models.CharField(blank=True, default=u'', max_length=200)
    birthday = models.DateField(blank=True, null=True)
    about = models.CharField(blank=True, default=u'',  max_length=100)
    achievements = models.TextField(default=u'{}')
