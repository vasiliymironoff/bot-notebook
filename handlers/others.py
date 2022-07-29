from textwrap import dedent
from aiogram import Dispatcher
from aiogram.types import Message
from data import database

info = dedent("""\
                Telegram bot для ведения дневника
                
                <b>Команды</b>
                /new_category - создание новой категории
                /delete_category - удаляет выбранную категорию
                
                /new_note - создание новой записи
                /read_note - чтение одной заметки
                /read_all_notes - чтение всех заметок
                
                /help - выводить это сообщение
                """)


async def start(message: Message):
    telegram_id = message.from_user.id
    if telegram_id not in database.get_all_telegram_id():
        database.create_user(telegram_id)
    await message.answer(info)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
