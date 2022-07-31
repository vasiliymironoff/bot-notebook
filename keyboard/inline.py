from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import database


def get_title_keyboard(telegram_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for id, title in database.select_title(telegram_id):
        keyboard.insert(InlineKeyboardButton(text=title, callback_data=title))
    return keyboard
