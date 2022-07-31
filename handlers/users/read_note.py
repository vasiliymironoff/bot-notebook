from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import database
from data.models import Note
from keyboard import get_title_keyboard


class ReadNote(StatesGroup):
    buttons = State()


async def choice_note(message: Message):
    await ReadNote.buttons.set()
    await message.answer("Выберете название заметки", reply_markup=get_title_keyboard(message.from_user.id))


async def print_one_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    telegram_id = callback.from_user.id
    title = callback.data
    note = database.select_note(telegram_id, title)
    await print_note(callback.message, note)


async def print_all_notes(message: Message):
    for note in database.select_notes(message.from_user.id):
        await print_note(message, note)


async def find_note(message: Message):
    note = database.select_note(message.from_user.id, title=message.text)
    if note is not None:
        await print_note(message, note)
    else:
        await message.answer('Записи с таким названием нет')


async def print_note(message, note: Note):
    assert note is not None, 'Записки почему-то нет'
    if note.photo is None:
        await message.answer(str(note))
    else:
        await message.answer_photo(note.photo, str(note))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(choice_note, commands='read_note')
    dp.register_callback_query_handler(print_one_note, state=ReadNote.buttons)
    dp.register_message_handler(print_all_notes, commands='read_all_notes')
    dp.register_message_handler(find_note)
