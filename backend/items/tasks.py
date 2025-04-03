import os
import logging
from celery import shared_task
from celery.schedules import crontab

from items.management.commands.telegram import send_message_sync
from items.service import TelegramRentalInfo

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def tomorrow_schedule(self):
    try:
        telegram_data = TelegramRentalInfo.format_tomorrow_rentals()
        chat_id = os.getenv('CHAT_ID')
        if not chat_id:
            logger.error("CHAT_ID environment variable is not set")
            return

        send_message_sync(message=telegram_data, chat_id=chat_id)
    except Exception as e:
        logger.error(f"Error in tomorrow_schedule: {str(e)}", exc_info=True)
        raise self.retry(exc=e, countdown=60)
