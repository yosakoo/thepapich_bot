from aiogram import executor
from create_bot import dp
from handlers import client, admin
from data_base import sqlite_db


async def on_startup(_):
    print("Bot is ready to work !")
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
