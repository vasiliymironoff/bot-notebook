
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import database


def get_category_keyboard(telegram_id) -> ReplyKeyboardMarkup:
    category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for category in database.select_name_category(telegram_id):
        category_keyboard.add(KeyboardButton(text=category))

    category_keyboard.add(KeyboardButton(text='Без категории'))

    return category_keyboard
