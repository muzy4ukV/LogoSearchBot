from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from states import MediaProcessing

import os
import markdown as md
from database import models as dbm


async def return_result(message: Message, state: FSMContext, user: dbm.User):
    await state.set_state(MediaProcessing.processing_media)
    list_photos: list[str] = os.listdir(user.data_folder)
    if len(list_photos) > 1:
        album_builder = MediaGroupBuilder(
            caption="yours photo"
        )
        for photo in list_photos:
            file_path = os.path.join(user.data_folder, photo)
            album_builder.add(
                type="photo",
                media=FSInputFile(file_path)
            )
        await message.answer_media_group(media=album_builder.build())
    elif len(list_photos) == 1:
        image_from_pc = FSInputFile(os.path.join(user.data_folder, list_photos[0]))
        await message.answer_photo(
            image_from_pc
        )
    else:
        await message.answer(
            "You didn't uploaded any files 🤷‍♂️"
        )
    await state.clear()


async def warning_send_media(message: Message):
    await message.answer(
        text=md.text(
            "You need to send your media at first 🤌",
            md.text("To do this write", md.bold("/start"), "command"),
            sep="\n"
        )
    )