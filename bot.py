import time
import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
import os



WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    kb = [
        [
            types.KeyboardButton(text="1 уровень"),
            types.KeyboardButton(text="2 уровень"),
            types.KeyboardButton(text="3 уровень")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    await message.answer(f'Привет, {user_full_name}, я умный Python-бот, настолько умный, что могу помочь тебе '
                         'с олимпиадными заданиями 5 класса по математике. Выбери уровень сложности. Чем выше тем сложнее',
                         reply_markup=keyboard)

@dp.message_handler(lambda message: message.text and '1 уровень' in message.text)
async def text_handler(message: types.Message):
    await message.reply('Раз ты выбрал(а) первый уровень, то ты ничего не знаешь, тебе уже не помочь, сдайся.')

@dp.message_handler(lambda message: message.text and '2 уровень' in message.text)
async def text_handler(message: types.Message):
    await message.reply('Раз второй уровень, значит что-нибудь, да знаешь, и так олимпиаду напишешь.')

@dp.message_handler(lambda message: message.text and '3 уровень' in message.text)
async def text_handler(message: types.Message):
    await message.reply(
        'Ты выбрал(а) максимальный уровень сложности, значит ты все знаешь, зачем тебе нужны эти задания...')




while True:
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
