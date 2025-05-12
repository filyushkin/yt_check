from django.db import models

# Create your models here.

from django.db import models

class Channel(models.Model):
    pseudonym = models.CharField(max_length=255, unique=True)  # Псевдоним канала
    name = models.CharField(max_length=255)  # Имя канала
    url = models.URLField()  # Ссылка на канал
    is_live = models.BooleanField(default=False)  # Добавьте поле для статуса эфира

    def __str__(self):
        return self.pseudonym

