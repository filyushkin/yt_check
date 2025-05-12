from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Channel
from .forms import ChannelForm
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import googleapiclient.discovery
from .utils import check_stream_is_live

# load_dotenv()
# api_key = os.getenv('YOUTUBE_API_KEY')

# Проверка существования канала
def check_youtube_channel(pseudonym):
    if not pseudonym.startswith('@'):
        pseudonym = '@' + pseudonym

    url = f'https://www.youtube.com/{pseudonym}'
    response = requests.get(url)

    if response.status_code == 200 and 'This channel does not exist' not in response.text:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find("title")
        channel_name = title_tag.text.replace(" - YouTube", "").strip() if title_tag else "Неизвестно"
        return channel_name, url

    return None, None

# Проверка активности трансляции
def check_stream_status(request):
    if request.method == 'POST':
        pseudonym = request.POST.get('pseudonym', '')
        if not pseudonym:
            messages.error(request, 'Псевдоним канала не передан.')
        else:
            is_live = check_stream_is_live(pseudonym)
            if is_live:
                messages.success(request, 'На канале идёт прямая трансляция.')
            else:
                messages.error(request, 'В настоящий момент прямой трансляции нет.')

        form = ChannelForm(initial={'pseudonym': pseudonym})
        return render(request, 'channels/index.html', {'form': form})
    return redirect('index')

def index(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            pseudonym = form.cleaned_data['pseudonym']
            name, url = check_youtube_channel(pseudonym)

            if name and url:
                if not Channel.objects.filter(pseudonym=pseudonym).exists():
                    Channel.objects.create(pseudonym=pseudonym, name=name, url=url)
                    messages.success(request, 'Канал найден, информация добавлена в базу данных.')
                else:
                    messages.warning(request, 'Информация о данном канале была занесена в базу данных ранее.')
            else:
                messages.error(request, 'Канала с таким псевдонимом не существует.')
        return render(request, 'channels/index.html', {'form': form})
    else:
        form = ChannelForm()

    return render(request, 'channels/index.html', {'form': form})

def check_stream_status(request):
    if request.method == 'POST':
        pseudonym = request.POST.get('pseudonym', '')
        if not pseudonym:
            messages.error(request, 'Псевдоним канала не передан.')
        else:
            is_live = check_stream_is_live(pseudonym)
            if is_live:
                messages.success(request, 'На канале идёт прямая трансляция.')
            else:
                messages.error(request, 'В настоящий момент прямой трансляции нет.')

        form = ChannelForm(initial={'pseudonym': pseudonym})
        return render(request, 'channels/index.html', {'form': form})
    return redirect('index')

# Остальные представления
def channels_list(request):
    channels = Channel.objects.all()
    return render(request, 'channels/channels_list.html', {'channels': channels})

def delete_channel(request, channel_id):
    if request.method == 'POST':
        channel = get_object_or_404(Channel, id=channel_id)
        channel.delete()
    return redirect('channels_list')

def tasks(request):
    return render(request, 'channels/tasks.html')

def files(request):
    return render(request, 'channels/files.html')
