from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import markdown as md
import os

from database import models as dbm
from keyboards.keyboards import get_main_keyboard


def clear_folder(path: str):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


async def start_message(message: Message, state: FSMContext, user: dbm.User):
    await message.answer(
        text=md.text(
            md.text("I'm glad you decided to use me 😊"),
            md.text("Send /menu command to detect logo"),
            sep='\n'
        )
    )


async def get_menu(message: Message):
    await message.answer(
        text="This is main menu\. Choose what you want to do:",
        reply_markup=get_main_keyboard()
    )


