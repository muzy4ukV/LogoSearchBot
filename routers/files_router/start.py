from main_keyboard import get_main_keyboard
from aiogram.types import Message


async def start_message(message: Message):
    await message.answer(
        "Hi! This is LogoSearch bot. Choose what you want to do:\n\n"
        "\U00002b07 - Download your file to bot\n\n"
        "\U00002b06 - Get your file from bot\n\n"
        "\U0001F517 - Download your file from URL",
        reply_markup=get_main_keyboard()
    )

