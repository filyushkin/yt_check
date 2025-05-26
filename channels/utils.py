import logging
import os
import requests
from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)
logger.setLevel('INFO')

load_dotenv()

YT_API_KEY = os.getenv('YOUTUBE_API_KEY')


def get_channel_id(pseudonym):
    """
    Получение ID канала по @handle, используя YouTube Data API v3
    """
    if not pseudonym.startswith('@'):
        pseudonym = '@' + pseudonym

    url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={pseudonym[1:]}&key={YT_API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']
    except requests.RequestException as e:
        logger.error("Ошибка запроса к YouTube API:", e)

    return None


def check_stream_is_live(pseudonym):
    """
    Проверка, идет ли трансляция на канале, используя YouTube Data API v3
    """
    return get_live_streams_count(pseudonym) > 0


def get_live_streams_count(pseudonym):
    """
    Получение количества прямых трансляций на канале по псевдониму, используя YouTube Data API v3
    """
    channel_id = get_channel_id(pseudonym)
    if not channel_id:
        return 0

    url = (
        'https://www.googleapis.com/youtube/v3/search'
        f'?part=snippet&channelId={channel_id}&eventType=live&type=video&key={YT_API_KEY}'
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return len(data.get('items', []))
    except requests.RequestException as e:
        logger.error("Ошибка запроса к YouTube API:", e)

    return 0
