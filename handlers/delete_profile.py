from aiogram.types import Message

import shutil

from database import models as dbm

import markdown as md


async def delete_user_data(message: Message, user: dbm.User):
    shutil.rmtree(f"users/{user.hash_id}")
    user.delete()
    await message.answer(
        text=md.text("Your deleted", md.bold("all your information"), "from this bot\!\n",
                     "To use this bot again, press any button or write any command or message")
    )

