from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_keyboard(items: list[str]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=item, callback_data=item))
        builder.adjust(1)
    return builder
