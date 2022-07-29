from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import database


def get_title_keyboard(telegram_id):
    keyboard = InlineKeyboardMarkup()

    for title in database.select_title(telegram_id):
        keyboard.insert(InlineKeyboardButton(text=title[0], callback_data=title[0]))

    return keyboard
