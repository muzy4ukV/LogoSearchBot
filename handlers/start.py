from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import markdown as md
from states import MediaProcessing
import os


async def start_message(message: Message, state: FSMContext):
    # clearing previous media
    await state.clear()
    directory_path = f"users/{message.from_user.id}"
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # setting new state
    await state.set_state(MediaProcessing.sending_media)
    await message.answer(
        text=md.text(
            md.text("I'm glad you decided to use me 😊"),
            md.text("Now, send from", md.bold("1 to 5"), "photos in this chat and write /run command"),
            sep='\n'
        )
    )
