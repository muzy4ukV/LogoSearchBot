from aiogram import Router, F
from aiogram.filters import CommandStart
from .start import start_message

router = Router()
router.message.filter(F.chat.type == "private")

router.message.register(start_message, CommandStart())



'''
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! Please send your photo!")


@dp.message(F.text == "лох")
async def lox(message: types.Message):
    await message.reply("Сам ти лох!")


@dp.message(Command("image_url"))
async def send_photo_url(message: types.Message):
    image = URLInputFile(
        "https://www.techsmith.com/blog/wp-content/uploads/2022/03/resize-image.png"
    )
    result = await message.answer_photo(
        image,
        caption="Image by URL"
    )
    global img_url
    img_url = result.photo[-1].file_id
    await message.answer(f"Id of image {img_url}")


@dp.message(Command("saved_image"))
async def send_saved_image(message: Message):
    await message.answer_photo(
        img_url
    )
'''

