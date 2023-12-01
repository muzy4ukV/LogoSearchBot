from main_keyboard import get_main_keyboard
from aiogram.types import Message


async def start_message(message: Message):
    await message.answer(
        "Hi. This is LogoSearch bot. Choose what you want to do!",
        reply_markup=get_main_keyboard()
    )