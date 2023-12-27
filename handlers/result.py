from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder


from states import MediaProcessing
from yolov5 import detect
import markdown as md
from database import models as dbm
from .start import clear_folder, get_menu

import os
import asyncio


async def run_model(callback: CallbackQuery, user: dbm.User):
    if len(os.listdir(user.data_folder)) == 0:
        await callback.answer(
            text="You need to send your media at first 🤌",
            show_alert=True
        )
        return
    clear_folder(user.result_folder)
    await asyncio.to_thread(
        detect.run,
        weights="weights/full_dataset.pt",
        source=user.data_folder,
        conf_thres=user.sens_level,
        project=f"users/{user.user_id}",
        classes=0,
        name='result',
        exist_ok=True,
        hide_labels=not user.show_labels
    )
    await send_result(callback.message, user)
    await callback.message.delete()
    await get_menu(callback.message)


async def send_result(message: Message, user: dbm.User):
    media_list: list[str] = os.listdir(user.result_folder)
    if len(media_list) > 1:
        album_builder = MediaGroupBuilder(
            caption=md.text(
                "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                "do this, click", md.bold("\"Configure the model\""), "in menu"
            )
        )
        for media in media_list:
            file_path = os.path.join(user.result_folder, media)
            if media[-3:] in ('jpg', 'png'):
                album_builder.add(
                    type="photo",
                    media=FSInputFile(file_path)
                )
            else:
                album_builder.add(
                    type="video",
                    media=FSInputFile(file_path)
                )
        await message.answer_media_group(media=album_builder.build())
    elif len(media_list) == 1:
        file_type = media_list[0].split('.')[1].lower()
        media_from_pc = FSInputFile(os.path.join(user.result_folder, media_list[0]))
        if file_type in ('jpg', 'png'):
            await message.answer_photo(
                media_from_pc,
                caption=md.text(
                    "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                    "do this, click", md.bold("\"Configure the model\""), "in menu"
                )
            )
        else:
            await message.answer_video(
                media_from_pc,
                caption=md.text(
                    "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                    "do this, click", md.bold("\"Configure the model\""), "in menu"
                )
            )
    else:
        await message.answer(
            "Smth went wrong 🤷‍♂️"
        )



