from django.db import models

from datetime import datetime

class ProcessImageManager(models.Manager):
    def create(self, *args, **kwargs):
        current_datatime = datetime.now()
        return super().create(created_at=current_datatime, updated_at=current_datatime, *args, **kwargs)

# Create your models here.
class ProcessImage(models.Model):
    image_src = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = ProcessImageManager
