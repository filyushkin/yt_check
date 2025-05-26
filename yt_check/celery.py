# yt_check/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_check.settings')

app = Celery('yt_check')

# Загружаем конфигурацию Celery из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи во всех приложениях
app.autodiscover_tasks()

# Расписание периодических задач
app.conf.timezone = 'UTC'  # или 'Europe/Minsk' — если нужно локальное время
app.conf.beat_schedule = {
    'update-channels-streams-count-every-5-minutes': {
        'task': 'channels.tasks.update_channels_streams_count',
        'schedule': crontab(minute='*/5'),
    },
}
