import sqlite3 as sq
from create_bot import *
from keyboards import kb_client, kb_admin
from config import ADMIN


def sql_start():
    global base, cur
    base = sq.connect("papich.db")
    cur = base.cursor()
    if base:
        print("Database connected ok!")
    base.execute("CREATE TABLE IF NOT EXISTS menu(sticker, name TEXT, description TEXT, price TEXT)")
    base.execute("CREATE TABLE IF NOT EXISTS profile(username TEXT)")
    base.execute("CREATE TABLE IF NOT EXISTS users_id(user_id TEXT PRIMARY KEY)")
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sql_send_mess(state):
        async with state.proxy() as data:
                for user_id in cur.execute("SELECT user_id FROM users_id").fetchall():
                    chat_id = user_id[0]  # найс чат гпт
                    await bot.send_sticker(chat_id=chat_id, sticker=data['sticker'])
                    await bot.send_message(chat_id=chat_id,
                                           text=f"Новый товар !\nИмя: {data['name']}\nОписание: {data['description']}\nЦена: {data['price']}", reply_markup=kb_client)


async def sql_read(message):
    for ret in cur.execute("SELECT * FROM menu").fetchall():
        if message.from_user.id in ADMIN:
            await bot.send_sticker(chat_id=message.from_user.id, sticker=ret[0])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"-----------------------------------------------------\nИмя: {ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]}\n-----------------------------------------------------",
                                   reply_markup=kb_admin)
        else:
            await bot.send_sticker(chat_id=message.from_user.id, sticker=ret[0])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"-----------------------------------------------------\nИмя: {ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]}\n-----------------------------------------------------",
                                   reply_markup=kb_client)


async def create_profile(username):
    user = cur.execute("SELECT 1 FROM profile WHERE username == '{key}'".format(key=username)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?)", (username,))
        base.commit()


async def sql_read_users(message):
    if message.from_user.id in ADMIN:
        await bot.send_message(chat_id=message.from_user.id, text="Username: ")
        for ret in cur.execute("SELECT * FROM profile").fetchall():
           await bot.send_message(chat_id=message.from_user.id, text=f"{ret[0]}")
    else:
        await message.answer("Вы не админ")


async def sql_read_users_id(message):
    if message.from_user.id in ADMIN:
        await bot.send_message(chat_id=message.from_user.id, text="Users_ID: ")
        for ret in cur.execute("SELECT * FROM users_id").fetchall():
            await bot.send_message(chat_id=message.from_user.id, text=f"{ret[0]}")


async def create_profile_id(user_id):
    user = cur.execute("SELECT 1 FROM users_id WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users_id VALUES(?)", (user_id,))
        base.commit()


async def sql_delete(message) -> None:
    if message.from_user.id in ADMIN:
        cur.execute("DELETE FROM menu")
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJzUdkvru6M-28M9SQaxHujXMMdPtDfwAC9xUAAjFv6Urd5ZP3yYZv0y8E")
        await bot.send_message(chat_id=message.from_user.id, text="Таблица очищена")

        base.commit()
    else:
        await message.answer("Вы не админ !")
