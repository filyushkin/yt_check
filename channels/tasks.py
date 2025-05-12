# channels/tasks.py
from celery import shared_task
from .models import Channel
from .views import check_stream_status
from .utils import check_stream_is_live

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
