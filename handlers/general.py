from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from misc import bot, dp
from handlers.keyboard import kb_client, kb_admin, kb_support, kb_reviews, back
import psycopg


class States_(StatesGroup):
    att = State()

conn = psycopg.connect(host='localhost')
conn.autocommit = True
try:
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, user_id bigint UNIQUE, username text, admin int);""")
        print(f'[DATABASE] База данных была успешно создана.')
except psycopg.errors.DuplicateDatabase:
    pass

async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Привет, @{message.from_user.username}',
        reply_markup=kb_client
    )
    user_id = message.from_user.id
    username = message.from_user.username
    conn = psycopg.connect(host='localhost')
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO users (user_id, username, admin) VALUES (%s, %s, %s)""",
                        (user_id, username, 0))
            conn.commit()
    except psycopg.errors.UniqueViolation:
        pass
    except psycopg.errors.InFailedSqlTransaction:
        pass

async def bots(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Статус ботов на данный момент:\n'
             f'@itmynamesbot 🔴\n'
             f'@mnogozlostishop 🔴',
        reply_markup=kb_client
    )

async def adm(message: types.Message):
    try:
        with conn.cursor() as cur:
            checkAdm = cur.execute("SELECT user_id FROM users WHERE admin=1;")
            rows = checkAdm.fetchall()
            for row in rows:
                row = row[0]
    except:
        pass
    if message.chat.id == row:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'Вы вошли в ⚙️ Администрирование',
            reply_markup=kb_admin
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text='К сожалению у вас нет доступа к ⚙️ Админке',
            reply_markup=kb_client
        )
        await bot.send_sticker(
            chat_id=message.chat.id,
            sticker=r'CAACAgIAAxkBAAEHgDJj1ndpJzVj4iugsOQyFylOI3nGhgACbRQAAvh48Ev_35tLbqKxRy0E'# еж
        )

async def support(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'По всем вопросам, недочетам и услугам\.',
        reply_markup=kb_support
    )
    await bot.send_video(
        chat_id=message.chat.id,
        video=r'https://s9.gifyu.com/images/animation042e91e4ca542b38.gif'
    )

async def reviews(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Узнать отзывы покупателей по ссылке ниже\.',
        reply_markup=kb_reviews
    )

async def back(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'В главное меню',
        reply_markup=kb_client
    )

@dp.message_handler(state=States_.att)
async def att(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['att'] = message.text
        data = dict(data)
        data = data['att']
        with conn.cursor() as cur:
            list_user_id = cur.execute("SELECT user_id FROM users")
            rows = list_user_id.fetchall()
            for row in rows:
                row = row[0]
        await bot.send_message(
            chat_id=row,
            text=f'{data}'
        )
    await state.finish()

async def att_set(message: types.Message):
    with conn.cursor() as cur:
        list_user_id = cur.execute("SELECT user_id FROM users")
        rows = list_user_id.fetchall()
        for row in rows:
            row = row[0]
    if message.chat.id == row:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Введите текст:',
        )
        await States_.att.set()


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(start, Text(equals=['/start']))
    dp.register_message_handler(adm, Text(equals=['/admin', '/adm', '⚙️ Администрирование']))
    dp.register_message_handler(bots, Text(equals=['/bots', '🦾 Железяки']))
    dp.register_message_handler(att_set, Text(equals=['/attention', '/att', '🔤 Написать всем']))
    dp.register_message_handler(support, Text(equals=['/support', '💌 Связаться']))
    dp.register_message_handler(reviews, Text(equals=['/reviews', '🤝🏻 Отзывы']))
    dp.register_message_handler(back, Text(equals=['/back', 'Назад']))