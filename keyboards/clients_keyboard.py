from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_students_list = KeyboardButton('/Мои_ученики')
button_add_timetable = KeyboardButton('/Добавить_расписание')
button_timetable = KeyboardButton('/Расписание_занятий')
button_add_student = KeyboardButton('/Добавить_ученика(ученицу)')
button_student_delete = KeyboardButton('/Удалить_ученика')
button_delete_timetable = KeyboardButton('/Удалить_расписание')
button_cancel = KeyboardButton('/Отмена')


keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.row(button_students_list, button_add_timetable, button_timetable)\
    .add(button_add_student).add(button_cancel).add(button_student_delete)\
    .add(button_delete_timetable)