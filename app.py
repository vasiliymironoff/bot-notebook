from aiogram.types import BotCommand
from aiogram import executor
import handlers
from config import ADMIN_ID
from loader import bot, dp


bot_commands = [
        ('new_category', 'создание новой категории', ''),
        ('delete_category', 'удаляет выбранную категорию', ''),
        ('new_note', 'создание новой записи', ''),
        ('read_note', 'чтение одной заметки', ''),
        ('read_all_notes', 'чтение всех заметок', ''),
        ('help', 'выводить это сообщение', ''),
    ]


def get_commands():
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    return commands_for_bot


async def on_startup(_):
    await bot.send_message(ADMIN_ID, "Бот запущен")
    await bot.set_my_commands(commands=get_commands())


async def on_shutdown(_):
    await bot.send_message(ADMIN_ID, "Бот выключен")


def main():
    handlers.others.register_handlers(dp)
    handlers.users.register_handlers(dp)
    handlers.admin.register_handlers(dp)

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
