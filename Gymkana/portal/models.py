import os

from django.db import models
from django.dispatch import receiver
from django.utils import timezone

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

"""
Deletes file from filesystem
when corresponding `MediaFile` object is deleted.
"""
@receiver(models.signals.post_delete, sender=New)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image and instance.image.name != 'default.jpg':
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

class Event(BaseItem):
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)