from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client, kb_admin
from data_base import sqlite_db
from config import ADMIN


async def start_cmd(message: types.Message):
    if message.from_user.id in ADMIN:
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJy_pkvjo5HTuMN49vtkyg0crMmkBiAANpKwACh754Sx94-20fuO5sLwQ",
                               reply_markup=kb_admin)
        await message.answer("Добро пожаловать !")
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)
    else:
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJy_pkvjo5HTuMN49vtkyg0crMmkBiAANpKwACh754Sx94-20fuO5sLwQ",
                               reply_markup=kb_client)
        await message.answer("Добро пожаловать !")
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)


async def help_cmd(message: types.Message):
    if message.from_user.id in ADMIN:
        await bot.send_sticker(chat_id=message.from_user.id,
                           sticker="CAACAgIAAxkBAAEJzBlkvlObdzzE6BAQhmpBWck3nNdYvgACYRsAAvLI8Uo65IfltJW8-C8E",
                           reply_markup=kb_admin)
        await message.answer("Привет, с чем могу помочь хозяин?")
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)
    else:
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJzBlkvlObdzzE6BAQhmpBWck3nNdYvgACYRsAAvLI8Uo65IfltJW8-C8E",
                               reply_markup=kb_client)
        await message.answer("Привет, с чем могу помочь ?")
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)


async def place_cmd(message: types.Message):
    if message.from_user.id in ADMIN:
        await bot.send_sticker(chat_id=message.from_user.id, sticker="CAACAgIAAxkBAAEJzBNkvkibzSe56z0ylQLmGucoTx9mJgACJRYAAiAg-Uoa21_9nnLxby8E")
        await bot.send_message(chat_id=message.from_user.id, text="Наш адрес - Улица Пушкина, дом Колотушкина", reply_markup=kb_admin)
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)
    else:
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJzBNkvkibzSe56z0ylQLmGucoTx9mJgACJRYAAiAg-Uoa21_9nnLxby8E")
        await bot.send_message(chat_id=message.from_user.id, text="Наш адрес - Улица Пушкина, дом Колотушкина",
                               reply_markup=kb_client)
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)


async def menu_cmd(message: types.Message):
        await sqlite_db.sql_read(message)
        await sqlite_db.create_profile(username=message.from_user.username)
        await sqlite_db.create_profile_id(user_id=message.from_user.id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(help_cmd, commands=['help'])
    dp.register_message_handler(place_cmd, commands=['place'])
    dp.register_message_handler(menu_cmd, commands=['menu'])

