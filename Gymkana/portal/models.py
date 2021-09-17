import os

from django.db import models
from django.utils import timezone
from uuid import uuid4
from datetime import date

def path_and_rename(instance, filename):
        upload_to = ""
        name = filename.split('.')[0]
        ext = filename.split('.')[-1]
        now = instance.publish_date.strftime("%d-%m-%YT%H%M")
        filename = '{}{}.{}'.format(name, now, ext)
        return os.path.join(upload_to, filename)

class BaseItem(models.Model):
    title = models.CharField(max_length = 100, blank = False)
    subtitle = models.CharField(max_length = 200, blank = False)
    body = models.TextField(blank = False)

    class Meta:
        abstract = True

class New(BaseItem):
    publish_date = models.DateTimeField(default = timezone.now)
    image = models.ImageField(upload_to=path_and_rename, default ='default.jpg')

class Event(BaseItem):
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)