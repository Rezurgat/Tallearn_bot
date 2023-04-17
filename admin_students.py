from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base import sqlite_db


class AddStudent(StatesGroup):
    name = State()
    level = State()
    day = State()
    daytime = State()
    price = State()


"""Выход из состояния"""


async def state_cancel(message: types.Message, state=FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    await state.finish()
    await message.reply('OK')


"""Добавление нового ученика"""


async def st_start(message: types.Message):
     await AddStudent.name.set()
     await message.reply('Оо! У тебя новый ученик? Поздравляю, Буся! Напиши имя ученика (ну,или ученицы)')


"""Ловлю первый ответ и заношу в словарь"""


async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await AddStudent.next()
    await message.reply('Отлично! А какой у него/нее уровень владения языком?')


"""Уровень языка"""


async def load_level(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['level'] = message.text
    await AddStudent.next()
    await message.reply('Принято! По каким дням будете заниматься?')


"""Ввод дня занятий"""


async def load_day(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text
    await AddStudent.next()
    await message.reply('Хорошо! На какое время договорились?')

"""Ввод времени"""


async def load_daytime(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['daytime'] = message.text
    await AddStudent.next()
    await message.reply('Хорошо! А что по цене занятия?')


"""Цена"""


async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    await sqlite_db.sql_add_students(state)
    await state.finish()


async def del_student_callback(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_student_command(callback_query.data.replace('Удалить ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Удалить ", "")} больше не твой ученик ',\
                                show_alert=True)


async def delete_student(message: types.Message):
    read = await sqlite_db.delete_students_db()
    for stud in read:
        await message.answer(f'{stud[1]} '
                             f'\nУровень --> {stud[2]}'
                             f'\nДень --> {stud[3]}'
                             f'\nВремя --> {stud[4]}'
                             f'\nЦена --> {stud[5]}')
        await message.answer(text='Удалить ученика?', reply_markup=InlineKeyboardMarkup().\
                             add(InlineKeyboardButton(f'Удалить {stud[1]}', callback_data=f'Удалить {stud[1]}')))










