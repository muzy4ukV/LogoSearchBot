from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import markdown as md
import os

from states import MediaProcessing
from database import models as dbm


def clear_folder(path: str):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


async def start_message(message: Message, state: FSMContext, user: dbm.User):
    # clearing previous media
    await state.clear()
    clear_folder(user.data_folder)
    # setting new state
    await state.set_state(MediaProcessing.sending_media)
    await message.answer(
        text=md.text(
            md.text("I'm glad you decided to use me 😊"),
            md.text("Now, send from", md.bold("1 to 5"), "photos in this chat and write /run command"),
            sep='\n'
        )
    )
