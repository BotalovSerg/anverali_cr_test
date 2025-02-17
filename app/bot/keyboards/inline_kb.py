from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def save_task_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    butts = [
        InlineKeyboardButton(text="Save", callback_data="save_task"),
        InlineKeyboardButton(text="Cansel", callback_data="cansel_task"),
        InlineKeyboardButton(text="Edit", callback_data="edit_task"),
    ]
    kb_builder.row(*butts, width=2)

    return kb_builder.as_markup()
