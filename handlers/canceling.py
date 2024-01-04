from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import markdown as md

from .start import get_menu


async def cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="There nothing to cancel",
    )


async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Action cancelled ❌",
    )
    await get_menu(message)


async def cancel_sens_chosen(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=md.text(
            "Changing sensitivity cancelled ❌"
        )
    )
    await get_menu(message)


async def no_reply(message: Message):
    await message.reply("I don't know this command 🤷‍♂️")


async def warning(message: Message):
    await message.reply(
        text="To run any command you need to stop sending media\n"
             "To do this click on 'Stop sending media' button or send /cancel command"
    )


async def warning_cl(callback: CallbackQuery):
    await callback.answer(
        text="To run any command you need to stop sending media\n"
             "To do this send /cancel command",
        show_alert=True
    )
