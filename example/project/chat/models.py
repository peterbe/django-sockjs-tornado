import datetime
from django.db import models
from django.utils.timezone import utc

def now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class Message(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(default=now)
