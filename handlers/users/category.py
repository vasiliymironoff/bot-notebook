from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import database


class CategoryState(StatesGroup):
    name = State()


async def create_category(message: Message):
    await CategoryState.name.set()
    await message.answer("Введите название категории")


async def enter_name_category(message: Message, state: FSMContext):
    data = {'name_category': message.text.strip(), 'telegram_id': message.from_user.id}
    database.insert_category(data)
    await state.finish()
    await message.answer('Категория создана')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(create_category, commands='new_category')
    dp.register_message_handler(enter_name_category, state=CategoryState.name)

