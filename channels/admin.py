from django.contrib import admin

# Register your models here.
# yt_check/admin.py

from django.contrib import admin
from .models import Channel  # Импортируем вашу модель

# Регистрируем модель в админ-панели
admin.site.register(Channel)
