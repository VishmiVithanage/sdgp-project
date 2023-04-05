from django.db import models

from datetime import datetime

# Create your models here.
class ProcessImage(models.Model):
    image_src = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    prediction = models.CharField(max_length=300, default='NA')

    @staticmethod
    def create_with_current_datetime(*args, **kwargs):
        current_datetime = datetime.now()
        return ProcessImage.objects.create(created_at=current_datetime, updated_at=current_datetime, *args, **kwargs)