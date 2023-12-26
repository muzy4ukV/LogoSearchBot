from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import markdown as md


async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="There nothing to cancel",
    )


async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Command cancelled",
    )


async def cmd_cancel_sending_media(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=md.text(
            "Sending media cancelled ❌",
            md.text("Run", md.bold("/start"), "command to try again"),
            sep="\n"
        ),
    )


async def cancel_sens_chosen(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=md.text(
            "Changing sensitivity cancelled ❌",
            md.text("Run", md.bold("/start"), "command to make new request"),
            sep="\n"
        ),
    )


async def no_reply(message: Message):
    await message.answer("Sorry, I do not understand you")