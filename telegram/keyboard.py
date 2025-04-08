from aiogram import types

def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Правила игры", callback_data="z_info"),]# кнопки
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard