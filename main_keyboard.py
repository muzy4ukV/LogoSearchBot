from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="\U00002b07")
    kb.button(text="\U00002b06")
    kb.button(text="\U0001F517")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)