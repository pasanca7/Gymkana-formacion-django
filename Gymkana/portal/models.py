from django.db import models
from django.utils import timezone

class BaseItem(models.Model):
    title = models.CharField(max_length = 100, blank = False)
    subtitle = models.CharField(max_length = 200, blank = False)
    body = models.TextField(blank = False)

    class Meta:
        abstract = True

class New(BaseItem):
    publish_date = models.DateTimeField(default = timezone.now)
    image = models.ImageField(upload_to = '', default ='default.jpg')

class Event(BaseItem):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()