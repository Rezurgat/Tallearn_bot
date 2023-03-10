import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

"""Функция для взаимодействия с пользователем """

@dp.message_handler(commands=['start', 'help'])
async def send_welcome_message(message: types.Message):
    await message.reply('Привет!\n Я Tallearn_bot! Займемся делом!')


"""Команда запуска бота на LongPolling"""

executor.start_polling(dp, skip_updates=True)

