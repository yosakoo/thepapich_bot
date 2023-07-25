from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#************* №1 *************
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/place")
b3 = KeyboardButton("/menu")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2, b3)
