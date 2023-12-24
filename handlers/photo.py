from aiogram import Bot
from aiogram.types import Message
import markdown as md
import os


async def get_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"users/{message.from_user.id}/{message.photo[-1].file_id}.jpg"
    )
    num_of_media = len(os.listdir(f"users/{message.from_user.id}"))
    await message.answer(
        text=md.text("Uploaded", md.bold(f"{num_of_media} from 5"), "photos")
    )


async def get_file_photo(message: Message, bot: Bot):
    file_type = message.document.file_name.split('.')[1]
    if file_type in ('jpg', 'png', 'mp4'):
        await bot.download(
            message.document,
            destination=f"users/{message.from_user.id}/{message.document.file_id}.{file_type}"
        )
        num_of_media = len(os.listdir(f"users/{message.from_user.id}"))
        await message.answer(
            text=md.text("Uploaded", md.bold(f"{num_of_media} from 5"), "photos")
        )
    else:
        await message.answer(
            text=md.text(
                "You sent incorrect media type ❗️",
                md.text("Send media only in", md.bold(".jpg .png .mp4"), "format"),
                sep="\n"
            )
        )
