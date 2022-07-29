from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_BOT
from data.database import start_db


storage = MemoryStorage()
bot = Bot(TOKEN_BOT, parse_mode='html')
dp = Dispatcher(bot, storage=storage)
start_db()
