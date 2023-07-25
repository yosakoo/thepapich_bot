from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import kb_cancel, kb_client, kb_admin
from data_base import sqlite_db
from config import ADMIN


class FSMAdmin(StatesGroup):
    sticker = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await FSMAdmin.sticker.set()
        await message.reply('Загрузите стикер', reply_markup=kb_cancel)
    else:
        await message.reply("Вы не админ !")


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN:
        curren_state = await state.get_state()
        if curren_state is None:
            return
        await state.finish()
        await message.reply("Отправка была отменена !", reply_markup=kb_admin)
    else:
        curren_state = await state.get_state()
        if curren_state is None:
            return
        await state.finish()
        await message.reply("Отправка была отменена !", reply_markup=kb_client)


async def load_sticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sticker'] = message.sticker.file_id
    await FSMAdmin.next()
    await message.reply("Теперь укажите название: ", reply_markup=kb_cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введите описание: ", reply_markup=kb_cancel)


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Теперь укажите цену товару: ", reply_markup=kb_cancel)


async def load_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await sqlite_db.sql_send_mess(state)

        await state.finish()
    except ValueError:
        await message.answer("Вы ввели не число")
        await cancel_handler(message, state)


async def cmd_read(message: types.Message):
    await sqlite_db.sql_read_users(message)
    await sqlite_db.sql_read_users_id(message)


async def cmd_delete_sql(message: types.Message):
    await sqlite_db.sql_delete(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['Upload'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="cancel")
    dp.register_message_handler(cancel_handler, Text(equals="cancel", ignore_case=True), state="*")
    dp.register_message_handler(load_sticker, content_types=['sticker'], state=FSMAdmin.sticker)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cmd_delete_sql, commands=['delete_db'])
    dp.register_message_handler(cmd_read, commands=['users_read'])
