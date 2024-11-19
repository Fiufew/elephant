from celery import shared_task
from aiogram import Bot
import asyncio
from django.utils import timezone

from .models import Bid


TELEGRAM_BOT_TOKEN = '7774904564:AAF3VXreAZV2SM-Lc5-arwjfomJnaD1SBCg'
CHAT_ID = '1671979968'


async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)


def send_message_sync(message):
    asyncio.run(send_telegram_message(message))


@shared_task
def check_rental_expiration():
    bids = Bid.objects.all()
    expired_list = []
    bids_to_update = []
    for bid in bids:
        if bid.dropoff_time < timezone.now() and not bid.is_expired:
            expired_list.append(f'Заявка №{bid.id} истекла')
            bid.is_expired = True
            bids_to_update.append(bid)
    if expired_list:
        message = '\n'.join(expired_list)
        send_message_sync(message=message)
    if bids_to_update:
        Bid.objects.bulk_update(bids_to_update, ['is_expired'])
