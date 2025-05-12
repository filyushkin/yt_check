# yt_check/__init__.py
from __future__ import absolute_import, unicode_literals

# Это позволит Django автоматически загружать Celery, когда приложение стартует
from .celery import app as celery_app

__all__ = ('celery_app',)
