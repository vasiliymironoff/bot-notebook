from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import database
from keyboard import get_category_keyboard


class NoteState(StatesGroup):
    category = State()
    title = State()
    text = State()
    photo = State()


async def new_note(message: Message):
    await NoteState.category.set()
    await message.answer('Выберите категорию',
                         reply_markup=get_category_keyboard(message.from_user.id))


async def enter_category(message: Message, state: FSMContext):
    category_id = None
    for category in database.select_name_category(message.from_user.id):
        if category[1].lower() == message.text.strip().lower():
            category_id = category[0]
            break
    async with state.proxy() as data:
        data['category_id'] = category_id
    await NoteState.next()
    await message.answer("Введите название записи",
                         reply_markup=ReplyKeyboardRemove())


async def enter_title(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text.strip()
    await NoteState.next()
    await message.answer('Введите текст записи')


async def enter_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text.strip()
    await NoteState.next()
    await message.answer('Прикрепите фото')


async def enter_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        data['telegram_id'] = message.from_user.id
        database.insert_note(dict(data))
    await state.finish()
    await message.answer("Запись добавлена")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(new_note, commands='new_note')
    dp.register_message_handler(enter_category, state=NoteState.category)
    dp.register_message_handler(enter_title, state=NoteState.title)
    dp.register_message_handler(enter_text, state=NoteState.text)
    dp.register_message_handler(enter_photo, state=NoteState.photo, content_types=['photo'])
