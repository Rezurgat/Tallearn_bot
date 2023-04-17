import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('tallearn_db')
    cur = base.cursor()
    if base:
        print('Database connected')
    base.execute('CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'
                 'name TEXT, '
                 'level TEXT, '
                 'day TEXT, '
                 'daytime TEXT,'
                 'price TEXT);')
    base.execute('CREATE TABLE IF NOT EXISTS timetable(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, '
                 'day TEXT, '
                 'info TEXT);')
    base.commit()


async def sql_add_students(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO students VALUES (null, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_timetable(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO timetable VALUES (null, ?, ?)', tuple(data.values()))
        base.commit()


async def send_me_my_students(message):
    for stud in cur.execute('SELECT * FROM students').fetchall():
        await message.answer(f'{stud[1]} '
                             f'\nУровень --> {stud[2]}'
                             f'\nДень --> {stud[3]}'
                             f'\nВремя --> {stud[4]}'
                             f'\nЦена --> {stud[5]}')


async def my_timetable(message):
    timetable_days = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
    for days in cur.execute('SELECT * FROM timetable').fetchall():
        if message.text.replace('/', '') in timetable_days and message.text.replace('/', '') == days[1]:
            await message.answer(f'{days[2]}')
        else:
            await message.answer(f'Расписание на {message.text} не заполнено. Займись этим, бублик!')


async def delete_students_db():
    return cur.execute('SELECT * FROM students').fetchall()


async def delete_timetable_db():
    return cur.execute('SELECT * FROM timetable').fetchall()


async def sql_delete_student_command(data):
    cur.execute('DELETE FROM students WHERE name == ?', (data,))
    base.commit()


async def sql_delete_timetable_command(data):
    cur.execute('DELETE FROM timetable WHERE day == ?', (data,))
    base.commit()


