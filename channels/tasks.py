# channels/tasks.py
from celery import shared_task
from .models import Channel
from .views import check_stream_status
from .utils import check_stream_is_live
import requests
from bs4 import BeautifulSoup

"""
@shared_task
def update_stream_status():
    channels = Channel.objects.all()
    for channel in channels:
        is_live = check_stream_status(channel.pseudonym)
        channel.is_live = is_live
        channel.save()
"""

@shared_task
def update_channels_live_status():
    for channel in Channel.objects.all():
        channel.is_live = check_stream_is_live(channel.pseudonym)
        channel.save()

@shared_task(name='channels.tasks.update_channels_streams_count')
def update_channels_streams_count():
    for channel in Channel.objects.all():
        try:
            count = get_live_streams_count(channel.youtube_url)
            channel.current_streams_count = count
            channel.save()
        except Exception as e:
            print(f'Ошибка при обновлении канала {channel.name}: {e}')

def get_live_streams_count(channel_url):
    # Преобразуем URL канала в URL с трансляциями
    if '/channel/' in channel_url:
        live_url = channel_url.rstrip('/') + '/streams'
    elif '/c/' in channel_url or '/@' in channel_url:
        # Особые случаи могут не поддерживаться без API, но можно попытаться
        live_url = channel_url.rstrip('/') + '/streams'
    else:
        raise ValueError("Некорректный формат URL канала")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(live_url, headers=headers)
    if response.status_code != 200:
        raise ValueError("Не удалось загрузить страницу трансляций")

    soup = BeautifulSoup(response.text, "html.parser")
    # YouTube часто использует Shadow DOM, поэтому ищем упрощённо
    return response.text.count('LIVE NOW')  # или другую эвристику