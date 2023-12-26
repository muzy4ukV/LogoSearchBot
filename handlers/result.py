from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from states import MediaProcessing
from yolov5 import detect
import markdown as md
from database import models as dbm
from .start import clear_folder

import os


async def return_result(message: Message, state: FSMContext, user: dbm.User):
    await state.set_state(MediaProcessing.processing_media)
    clear_folder(user.result_folder)
    detect.run(
        weights="weights/full_dataset.pt",
        source=user.data_folder,
        conf_thres=user.sens_level,
        project=f"users/{user.user_id}",
        classes=0,
        name='result',
        exist_ok=True,
    )
    await send_result_photo(message, user)
    await message.answer(
        text=md.text(
            md.text("In order to start the search again call the", md.bold("/start"), "command"),
            md.text(
                "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. To "
                "do this, write the", md.bold("/change_sens"), "command"
            ),
            sep='\n\n'
        )
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


async def last_result(message: Message, user: dbm.User):
    await send_result_photo(message, user)


async def send_result_photo(message: Message, user: dbm.User):
    list_photos: list[str] = os.listdir(user.result_folder)
    if len(list_photos) > 1:
        album_builder = MediaGroupBuilder(
            caption="here's your result"
        )
        for photo in list_photos:
            file_path = os.path.join(user.result_folder, photo)
            album_builder.add(
                type="photo",
                media=FSInputFile(file_path)
            )
        await message.answer_media_group(media=album_builder.build())
    elif len(list_photos) == 1:
        image_from_pc = FSInputFile(os.path.join(user.result_folder, list_photos[0]))
        await message.answer_photo(
            image_from_pc,
            caption="here's your result"
        )
    else:
        await message.answer(
            "Smth went wrong 🤷‍♂️"
        )
