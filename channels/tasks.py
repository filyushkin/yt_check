from celery import shared_task
from .models import Channel
from .utils import check_stream_is_live, get_live_streams_count
from logging import getLogger

logger = getLogger(__name__)
logger.setLevel('INFO')


@shared_task
def update_channels_live_status():
    for channel in Channel.objects.all():
        try:
            channel.is_live = check_stream_is_live(channel.pseudonym)
            channel.save(update_fields=["is_live"])
        except Exception as e:
            logger.error(f'Ошибка при обновлении статуса канала {channel.name}: {e}')


@shared_task(name='channels.tasks.update_channels_streams_count')
def update_channels_streams_count():
    for channel in Channel.objects.all():
        try:
            count = get_live_streams_count(channel.pseudonym)
            logger.info('channel name %s, count %s', channel.name, count)
            channel.current_streams_count = count
            channel.save(update_fields=["current_streams_count"])
        except Exception as e:
            logger.error(f'Ошибка при обновлении количества трансляций канала {channel.name}: {e}')
