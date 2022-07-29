from . import category
from . import create_note
from . import read_note


def register_handlers(dp):
    category.register_handlers(dp)
    create_note.register_handlers(dp)
    read_note.register_handlers(dp)
