from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from data import database


class CategoryState(StatesGroup):
    name = State()


async def create_category(message: Message):
    await CategoryState.name.set()
    await message.answer("Введите название категории")


async def enter_name_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.strip()
        data['telegram_id'] = message.from_user.id
    await database.insert_category(state)
    await state.finish()
    await message.answer(f'Категория {message.text} создана')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(create_category, commands='new_category')
    dp.register_message_handler(enter_name_category, state=CategoryState.name)

