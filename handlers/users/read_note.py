from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from data import database
from keyboard.inline import get_title_keyboard


class ReadNote(StatesGroup):
    buttons = State()


async def choice_note(message: Message):
    await ReadNote.buttons.set()
    await message.answer("Выберете название заметки", reply_markup=get_title_keyboard(message.from_user.id))


async def print_one_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await print_note(callback.message, database.select_notes(callback.from_user.id, callback.data)[0])


async def print_all_notes(message: Message):
    for note in database.select_notes(message.from_user.id):
        await print_note(message, note)


async def find_note(message: Message):
    note = database.select_notes(message.from_user.id, title=message.text)
    if len(note) > 0:
        await print_note(message, note[0])
    else:
        await message.answer('Записи с таким названием нет')


async def print_note(message, note):
    res = '\n'.join(note[:3])
    if note[3] is None:
        await message.answer(res)
    else:
        await message.answer_photo(note[3], res)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(choice_note, commands='read_note')
    dp.register_callback_query_handler(print_one_note, state=ReadNote.buttons)
    dp.register_message_handler(print_all_notes, commands='read_all_notes')
    dp.register_message_handler(find_note)
