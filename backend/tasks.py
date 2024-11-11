# ElephantRent/your_app_name/tasks.py
from celery import shared_task
from aiogram import Bot
from datetime import datetime, timedelta, timezone
from .models import Bid  # Предположим, что у вас есть модель Rental
import asyncio


TELEGRAM_BOT_TOKEN = '7774904564:AAF3VXreAZV2SM-Lc5-arwjfomJnaD1SBCg'
CHAT_ID = '1671979968'

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def send_message_sync(message):
    asyncio.run(send_telegram_message(message))


@shared_task
def check_rental_expiration():
    now = datetime.now()
    send_message_sync(message='kafka')
