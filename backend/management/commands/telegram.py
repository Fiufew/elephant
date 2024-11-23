from django.core.management.base import BaseCommand

from aiogram import Bot, types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from asgiref.sync import sync_to_async
import asyncio

from ...models import Bid

TELEGRAM_BOT_TOKEN = '7774904564:AAF3VXreAZV2SM-Lc5-arwjfomJnaD1SBCg'
CHAT_ID = '1671979968'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def bid_info(message: types.Message, bid):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Отклонить', callback_data=f'button1_{bid.id}')
    inline_btn_2 = InlineKeyboardButton('Принять', callback_data=f'button2_{bid.id}')
    inline_kb.add(inline_btn_1, inline_btn_2)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f'Booking request {bid.id}\n {bid.car_info}\n From: {bid.pickup_location}, {bid.pickup_time}\n To: {bid.dropoff_location} {bid.dropoff_time}\n Total:',
        reply_markup=inline_kb
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    action = data[0]
    bid_id = int(data[1])

    if action == 'button1':
        # Обновление статуса заявки
        bid = await sync_to_async(Bid.objects.get)(id=bid_id)
        bid.is_pending = False
        await sync_to_async(bid.save)()
        await bot.answer_callback_query(callback_query.id, text='Bid is now active.')
    elif action == 'button2':
        bid = await sync_to_async(Bid.objects.get)(id=bid_id)
        bid.is_pending = False
        bid.is_expired = False
        await sync_to_async(bid.save)()
        await bot.answer_callback_query(callback_query.id, text='You pressed Button 2')



def send_bid_sync(message, bid):
    asyncio.run(bid_info(message, bid))


def send_message_sync(message):
    asyncio.run(send_telegram_message(message))


class Command(BaseCommand):
    help = 'Start Telegram bot'

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)

# запускаем через python manage.py telegram