from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from states import MediaProcessing

import os
import markdown as md


async def return_result(message: Message, state: FSMContext):
    await state.set_state(MediaProcessing.processing_media)
    users_dir: str = f"users/{message.from_user.id}"
    list_photos: list[str] = os.listdir(users_dir)
    if len(list_photos) > 1:
        album_builder = MediaGroupBuilder(
            caption="yours photo"
        )
        for photo in list_photos:
            file_path = os.path.join(users_dir, photo)
            album_builder.add(
                type="photo",
                media=FSInputFile(file_path)
            )
        await message.answer_media_group(media=album_builder.build())
    elif len(list_photos) == 1:
        image_from_pc = FSInputFile(os.path.join(users_dir, list_photos[0]))
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