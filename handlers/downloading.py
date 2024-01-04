from typing import List, Dict

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, Downloadable
from sqlalchemy.orm import Mapped

import markdown as md
import os
import asyncio

from database import models as dbm
from states import MediaProcessing
from keyboards.keyboards import get_stop_keyboard
from .start import get_menu, clear_folder
from settings import settings

users_data: Dict[Mapped[int], List[Message]] = {}


async def start_downloading(callback: CallbackQuery, state: FSMContext, user: dbm.User):
    await callback.message.delete()
    await callback.message.answer(
        text=md.text(
            md.text("Send from", md.bold("1 to 5"), "media files in this chat"),
            md.text("Note\! ⚠️ Media must be only in", md.bold(".jpg .png .mp4 .mov"), "format"),
            md.text("Your video must be less than 15 sec long"),
            md.text("You can cancel this typing /cancel"),
            sep='\n'
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.to_thread(clear_folder, user.data_folder)
    await state.set_state(MediaProcessing.sending_media)
    await callback.answer()


async def check_max_num(path: str, message: Message):
    num = len(os.listdir(path))
    if num >= 5:
        await message.reply(
            text="You've already downloaded max number of media"
        )
        return True
    else:
        return False


async def get_photo(message: Message, bot: Bot, user: dbm.User, show_cancel: bool = True):
    if not await check_max_num(user.data_folder, message):
        await download_media(
            bot,
            message.photo[-1],
            f"{user.data_folder}/{message.photo[-1].file_id}.jpg"
        )
        if show_cancel:
            await show_stop_message(message, user)


async def get_document(message: Message, bot: Bot, user: dbm.User, show_cancel: bool = True):
    if not await check_max_num(user.data_folder, message):
        if not message.document.file_name:
            await message.reply(
                text=f"You sent media of unknown format, use only {md.bold('.jpg .png .mp4 .mov')} formats"
            )
        file_type = message.document.file_name.split('.')[1].lower()
        if file_type not in ('jpg', 'png', 'mp4', 'mov'):
            await message.reply(
                text=md.text(
                    "You sent incorrect media type ❗️",
                    md.text("Send media only in", md.bold(".jpg .png .mp4 .mov"), "format"),
                    sep="\n"
                )
            )
        elif message.document.file_size > settings.MAX_MEDIA_SIZE_BYTES:
            await message.reply(
                text="Media size must be less than 15mb\!"
            )
        else:
            await download_media(
                bot,
                message.document,
                f"{user.data_folder}/{message.document.file_id}.{file_type}"
            )
            if show_cancel:
                await show_stop_message(message, user)


async def get_video(message: Message, bot: Bot, user: dbm.User, show_cancel: bool = True):
    if not await check_max_num(user.data_folder, message):
        file_type = message.video.file_name.split('.')[1].lower()
        if message.video.duration > 15:
            await message.reply(
                text="Video is too long\! Your video must be less than 15 sec long"
            )
        elif file_type not in ('mp4', 'mov'):
            await message.reply(
                text=md.text(
                    "You sent incorrect media type ❗️",
                    md.text("Send media only in", md.bold(".jpg .png .mp4 .mov"), "formats"),
                    sep="\n"
                )
            )
        else:
            await download_media(
                bot,
                message.video,
                f"{user.data_folder}/{message.video.file_id}.{file_type}",
            )
            if show_cancel:
                await show_stop_message(message, user)


async def get_media_group(message: Message, bot: Bot, user: dbm.User, context: List[Message]):
    if context:
        for album_item in context:
            if album_item.photo:
                # Handle photo
                await get_photo(album_item, bot, user, show_cancel=False)
            elif album_item.document:
                # Handle document
                await get_document(album_item, bot, user, show_cancel=False)
            elif album_item.video:
                # Handle video
                await get_video(album_item, bot, user, show_cancel=False)
        await show_stop_message(message, user)
    context.clear()


async def download_media(bot: Bot, tg_object: Downloadable, destination: str):
    await bot.download(
        tg_object,
        destination=destination
    )


async def show_stop_message(message: Message, user: dbm.User):
    num_of_media = len(os.listdir(user.data_folder))
    stop_message = await message.answer(
        text=md.text("Downloaded", md.bold(f"{num_of_media} from 5"), "photos"),
        reply_markup=get_stop_keyboard()
    )
    if user.hash_id in users_data:
        users_data[user.hash_id].append(stop_message)
    else:
        users_data[user.hash_id] = [stop_message]


async def stop_downloading(callback: CallbackQuery, state: FSMContext, user: dbm.User):
    await state.clear()
    await callback.message.answer(
        text="Sending photos stopped 🛑"
    )
    if user.hash_id in users_data:
        for stop_message in users_data[user.hash_id]:
            await stop_message.delete()
        users_data[user.hash_id].clear()
    await get_menu(callback.message)


async def cancel_downloading(message: Message, state: FSMContext, user: dbm.User):
    await state.clear()
    await message.answer(
        text="Sending photos stopped 🛑"
    )
    if user.hash_id in users_data:
        for stop_message in users_data[user.hash_id]:
            await stop_message.delete()
        users_data[user.hash_id].clear()
    await get_menu(message)
