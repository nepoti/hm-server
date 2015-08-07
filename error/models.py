from django.db import models


class Error(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
