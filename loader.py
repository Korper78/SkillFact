from aiogram import Bot, Dispatcher
from os import getenv


bot_token = getenv("BOT_TOKEN")
bot = Bot(token=bot_token,
          parse_mode='HTML')
dp = Dispatcher()
