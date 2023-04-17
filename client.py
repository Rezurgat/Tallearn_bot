from aiogram import types

from data_base import sqlite_db
from keyboards import keyboard_client


"""Функция для взаимодействия с пользователем """


async def send_welcome_message(message: types.Message):
    await message.answer('Привет, Бублик!Я твой бот-помощник! Займемся делом!', reply_markup=keyboard_client)


async def students_list(message: types.Message):
    await sqlite_db.send_me_my_students(message)


async def send_me_my_timetable(message: types.Message):
    await sqlite_db.send_me_my_timetable(message)
