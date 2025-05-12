# yt_check/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_check.settings')

app = Celery('yt_check')

app.conf.beat_schedule = {
    'check-stream-status-every-5-minutes': {
        'task': 'channels.tasks.update_channels_live_status',  # <-- исправлено
        'schedule': crontab(minute='*/5'),
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
