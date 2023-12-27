from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
import markdown as md
import os
import asyncio

from database import models as dbm
from states import MediaProcessing
from keyboards.keyboards import get_stop_keyboard
from .start import get_menu


def clear_folder(path: str):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


async def start_downloading(callback: CallbackQuery, state: FSMContext, user: dbm.User):
    await callback.message.delete()
    await callback.message.answer(
        text=md.text(
            md.text("Send from", md.bold("1 to 5"), "media files in this chat"),
            md.text("Note\! ⚠️ Media must be only in", md.bold(".jpg .png .mp4 .mov"), "format"),
            md.text("You can cancel this but everything will be aborted"),
            sep='\n'
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.to_thread(clear_folder, user.data_folder)
    await state.set_state(MediaProcessing.sending_media)
    await state.update_data(media_num=0)
    await callback.answer()


async def check_max_num(path: str, message: Message):
    num = len(os.listdir(path))
    if num >= 5:
        await message.answer(
            text="You've already downloaded max number of media"
        )
        return True
    else:
        return False


async def get_photo(message: Message, bot: Bot, user: dbm.User):
    if not await check_max_num(user.data_folder, message):
        await download_media(
            message,
            bot,
            message.photo[-1],
            f"{user.data_folder}/{message.photo[-1].file_id}.jpg",
            user
        )


async def download_media(message: Message, bot: Bot, object, destination: str, user: dbm.User):
    await bot.download(
        object,
        destination=destination
    )
    num_of_media = len(os.listdir(user.data_folder))
    await message.answer(
        text=md.text("Downloaded", md.bold(f"{num_of_media} from 5"), "photos"),
        reply_markup=get_stop_keyboard()
    )


async def get_document(message: Message, bot: Bot, user: dbm.User):
    if not await check_max_num(user.data_folder, message):
        file_type = message.document.file_name.split('.')[1].lower()
        if file_type in ('jpg', 'png', 'mp4', 'mov'):
            await download_media(
                message,
                bot,
                message.document,
                f"{user.data_folder}/{message.document.file_id}.{file_type}",
                user
            )
        else:
            await message.answer(
                text=md.text(
                    "You sent incorrect media type ❗️",
                    md.text("Send media only in", md.bold(".jpg .png .mp4 .mov"), "format"),
                    sep="\n"
                )
            )


async def get_video(message: Message, bot: Bot, user: dbm.User):
    if not await check_max_num(user.data_folder, message):
        if message.video.duration > 15:
            await message.answer(
                text="Video is too long"
            )
        else:
            file_type = message.video.file_name.split('.')[1].lower()
            await download_media(
                message,
                bot,
                message.video,
                f"{user.data_folder}/{message.video.file_id}.{file_type}",
                user
            )


async def stop_downloading(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text="Sending photos stopped 🛑"
    )
    await callback.message.delete()
    await get_menu(callback.message)
