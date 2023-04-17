from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base import sqlite_db


class AddTimetable(StatesGroup):
    day = State()
    info = State()


async def tt_start(message: types.Message):
    await AddTimetable.day.set()
    await message.reply('Давай заполним расписание! Напиши день занятий!')


async def load_day(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text
    await AddTimetable.next()
    await message.reply('Отлично! Теперь напиши мне всю информацию по дню занятий! Учеников разделяй через Shift+Enter')


async def load_info(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text

    await sqlite_db.sql_add_timetable(state)
    await state.finish()


async def del_timetable_callback(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_timetable_command(callback_query.data.replace('Удалить ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Удалить ", "")}', show_alert=True)


async def delete_timetable(message: types.Message):
    read = await sqlite_db.delete_timetable_db()
    for days in read:
        await message.answer(f'{days[1]} '
                             f'\n{days[2]}')
        await message.answer(text='Удалить ?', reply_markup=InlineKeyboardMarkup().\
                             add(InlineKeyboardButton(f'Удалить {days[1]}', callback_data=f'Удалить {days[1]}')))