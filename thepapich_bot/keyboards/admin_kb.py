from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#************* №1 *************
cancel = KeyboardButton("/cancel")

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)

kb_cancel.insert(cancel)

#************* №2 *************
admin1 = KeyboardButton("/help")
admin2 = KeyboardButton("/place")
admin3 = KeyboardButton("/menu")
admin4 = KeyboardButton("/Upload")
admin5 = KeyboardButton("/delete_db")
admin6 = KeyboardButton("/users_read")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(admin1, admin2, admin3, admin4, admin5, admin6)
