from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from yolov5 import detect
import markdown as md
from database import models as dbm
from .start import clear_folder, get_menu
from settings import settings
from states import MediaProcessing

import os
import asyncio


async def run_model(callback: CallbackQuery, state: FSMContext, user: dbm.User):
    if len(os.listdir(user.data_folder)) == 0:
        await callback.answer(
            text="You need to send your media at first 🤌",
            show_alert=True
        )
        return
    await state.set_state(MediaProcessing.running_model)
    clear_folder(user.result_folder)
    await asyncio.to_thread(
        detect.run,
        weights="weights/full_dataset.pt",
        data="yolov5/datasets/custom_logo_dataset/data.yaml",
        source=user.data_folder,
        conf_thres=user.sens_level,
        project=f"users/{user.hash_id}",
        name='result',
        exist_ok=True,
        hide_labels=not user.show_labels,
        imgsz=(640, 640)
    )
    current_state = await state.get_state()
    if current_state == MediaProcessing.running_model:
        user.update(num_of_requests=user.num_of_requests + 1)
        await send_result(callback.message, user, user.result_folder)
        await get_menu(callback.message)
    await callback.message.delete()
    await state.clear()


async def send_result(message: Message, user: dbm.User, destination_folder: str):
    media_list: list[str] = os.listdir(destination_folder)
    if len(media_list) > 1:
        album_builder = MediaGroupBuilder()
        for media in media_list:
            file_path = os.path.join(destination_folder, media)
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
        if user.num_of_requests < settings.NUM_OF_REQUESTS_TO_HIDE_MSG:
            await message.answer(
                text=md.text(
                    "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                    "do this, click", md.bold("\"Configure the model\""), "in menu"
                )
            )
        else:
            await message.answer(
                text="Here's your result"
            )
    elif len(media_list) == 1:
        file_type = media_list[0].split('.')[1].lower()
        media_from_pc = FSInputFile(os.path.join(destination_folder, media_list[0]))
        if file_type in ('jpg', 'png'):
            await message.answer_photo(
                media_from_pc
            )
            if user.num_of_requests < settings.NUM_OF_REQUESTS_TO_HIDE_MSG:
                await message.answer(
                    text=md.text(
                        "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                        "do this, click", md.bold("\"Configure the model\""), "in menu"
                    )
                )
            else:
                await message.answer(
                    text="Here's your result"
                )
        else:
            await message.answer_video(
                media_from_pc
            )
            if user.num_of_requests < settings.NUM_OF_REQUESTS_TO_HIDE_MSG:
                await message.answer(
                    text=md.text(
                        "If the model did not find the logo, you can try to reduce the sensitivity level of the model\. \nTo "
                        "do this, click", md.bold("\"Configure the model\""), "in menu"
                    )
                )
            else:
                await message.answer(
                    text="Here's your result"
                )
    else:
        await message.answer(
            "Something went wrong 🤷‍♂️"
        )


async def get_last_media(callback: CallbackQuery, user: dbm.User):
    if len(os.listdir(user.data_folder)) == 0:
        await callback.answer(
            text="You didn't download media any media 😔",
            show_alert=True
        )
        return
    await send_result(callback.message, user, user.data_folder)
    await callback.message.delete()
    await get_menu(callback.message)
    await callback.answer()
