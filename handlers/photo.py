from aiogram import Bot
from aiogram.types import Message
import markdown as md
import os

from database import models as dbm


async def get_photo(message: Message, bot: Bot, user: dbm.User):
    await bot.download(
        message.photo[-1],
        destination=f"{user.data_folder}/{message.photo[-1].file_id}.jpg"
    )
    num_of_media = len(os.listdir(user.data_folder))
    await message.answer(
        text=md.text("Uploaded", md.bold(f"{num_of_media} from 5"), "photos")
    )


async def get_file_photo(message: Message, bot: Bot, user: dbm.User):
    file_type = message.document.file_name.split('.')[1]
    if file_type in ('jpg', 'png', 'mp4'):
        await bot.download(
            message.document,
            destination=f"{user.data_folder}/{message.document.file_id}.{file_type}"
        )
        num_of_media = len(os.listdir(user.data_folder))
        await message.answer(
            text=md.text("Uploaded", md.bold(f"{num_of_media} from 5"), "photos")
        )
    else:
        await message.answer(
            text=md.text(
                "You sent incorrect media type ❗️",
                md.text("Send media only in", md.bold(".jpg"), "format"),
                sep="\n"
            )
        )
