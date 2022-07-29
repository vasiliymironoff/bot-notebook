from loader import dp
from aiogram import executor
from handlers import admin, users, others


async def on_startup(_):
    pass


async def on_shutdown(_):
    pass


users.register_handlers(dp)
admin.register_handlers(dp)
others.register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
