from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import data
from config import TOKEN_BOT


storage = MemoryStorage()
bot = Bot(TOKEN_BOT, parse_mode='html')
dp = Dispatcher(bot, storage=storage)
database = data.Database()
