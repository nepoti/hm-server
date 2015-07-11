from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import UserProfile

class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, related_name='posts')
    likes = models.IntegerField(default=0)
    likes_ids = ArrayField(models.IntegerField())
    text = models.TextField(blank=True, default=u'')
    photos = ArrayField(models.URLField())
    locations = ArrayField(ArrayField(models.FloatField(), size=2))

