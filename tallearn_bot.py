import os

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

import client, admin_students, admin_timetable
from admin_students import AddStudent
from admin_timetable import AddTimetable

from data_base import sqlite_db

storage = MemoryStorage()

bot = aiogram.Bot(token=os.getenv('TOKEN'))
dp = aiogram.Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Tallearn_bot в онлайне!')
    sqlite_db.sql_start()

"""Основные команды"""

dp.register_message_handler(client.send_welcome_message, commands=['start'])
dp.register_message_handler(client.students_list, commands=['Мои_ученики'])
dp.register_message_handler(admin_students.state_cancel, commands=['Отмена'], state="*")
dp.register_message_handler(admin_students.state_cancel, Text(equals=['Отмена'], ignore_case=True), state='*')
dp.register_message_handler(admin_students.st_start, commands=['Добавить_ученика(ученицу)'], state=None)
dp.register_message_handler(admin_timetable.tt_start, commands=['Добавить_расписание'], state=None)
dp.register_message_handler(admin_students.delete_student, commands=['Удалить_ученика'])
dp.register_message_handler(admin_timetable.delete_timetable, commands=['Удалить_расписание'])
dp.register_callback_query_handler(admin_students.del_student_callback, lambda x: x.data and x.data.startswith('Удалить '))
dp.register_callback_query_handler(admin_timetable.del_timetable_callback, lambda x: x.data and x.data.startswith('Удалить '))
dp.register_message_handler(admin_students.load_name, state=AddStudent.name)
dp.register_message_handler(admin_students.load_level, state=AddStudent.level)
dp.register_message_handler(admin_students.load_day, state=AddStudent.day)
dp.register_message_handler(admin_students.load_daytime, state=AddStudent.daytime)
dp.register_message_handler(admin_students.load_price,  state=AddStudent.price)
dp.register_message_handler(admin_timetable.load_day, state=AddTimetable.day)
dp.register_message_handler(admin_timetable.load_info,  state=AddTimetable.info)
dp.register_message_handler(sqlite_db.my_timetable)


"""Команда запуска бота на LongPolling"""

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

