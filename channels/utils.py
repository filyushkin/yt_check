import requests
import os
from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_channel_id(pseudonym):
    """Получение ID канала по @handle (псевдониму), используя YouTube API"""
    if not pseudonym.startswith('@'):
        pseudonym = '@' + pseudonym

    api_key = YT_API_KEY
    url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={pseudonym[1:]}&key={api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']
    except requests.RequestException as e:
        print("Ошибка запроса:", e)

    return None


def check_stream_is_live(pseudonym):
    """Проверка, идет ли трансляция на канале"""
    channel_id = get_channel_id(pseudonym)
    if not channel_id:
        return False

    # URL для поиска активных трансляций на канале
    api_key = YT_API_KEY  # Вставьте ваш ключ API
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        # Если есть элементы в ответе, значит стрим идет
        if data.get('items'):
            return True
    except requests.RequestException:
        pass

    return False
