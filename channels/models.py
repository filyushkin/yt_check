# channels/models.py
from django.db import models

class Channel(models.Model):
    pseudonym = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    is_live = models.BooleanField(default=False)
    current_streams_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.pseudonym
