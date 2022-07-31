from aiogram import Dispatcher
from aiogram.types import Message
from app import bot_commands
from loader import database


async def start(message: Message) -> None:
    info = 'Telegram bot для ведения дневника\n<b>Команды</b>\n'
    for cmd in bot_commands:
        info += f'/{cmd[0]} - {cmd[1]}\n'
    telegram_id = message.from_user.id
    if telegram_id not in database.select_all_telegram_id():
        database.create_user(telegram_id)
    await message.answer(info)


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=['start', 'help'])
