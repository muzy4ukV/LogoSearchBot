from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks_data import ShowLabelData


def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Download new media 🖼",
        callback_data="download"
    ))
    builder.add(InlineKeyboardButton(
        text="Run model with uploaded media 🤖",
        callback_data="run"
    ))
    builder.add(InlineKeyboardButton(
        text="Сonfigure the model 🔧",
        callback_data="configure"
    ))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_stop_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Stop sending media",
        callback_data="stop"
    ))
    return builder.as_markup(resize_keyboard=True)


def get_conf_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Change sensitivity",
        callback_data="sensitivity"
    ))
    builder.button(
        text="Show labels on photo",
        callback_data=ShowLabelData(action="show_info")
    )
    return builder.as_markup(resize_keyboard=True)


def get_show_labels_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Show labels ✅",
        callback_data=ShowLabelData(action="change", value=True)
    )
    builder.button(
        text="Don't show labels ❌",
        callback_data=ShowLabelData(action="change", value=False)
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
