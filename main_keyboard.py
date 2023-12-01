from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Відправити фотографію до бота")
    kb.button(text="Отримати свою фотографію")
    kb.button(text="Отримати фотографію за посиланням")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)