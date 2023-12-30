import logging

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from states import ChangeSens
import markdown as md
from database import models as dbm
from keyboards.keyboards import get_conf_keyboard, get_show_labels_keyboard, get_main_keyboard
from .start import get_menu
from callbacks_data import ShowLabelData


async def start_configuration(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Choose action 👇",
        reply_markup=get_conf_keyboard()
    )
    await callback.answer()


async def start_sensitivity(callback: CallbackQuery, state: FSMContext, user: dbm.User):
    await callback.message.edit_text(
        text=md.text(
            md.text("If the quality of your photo is not high 😕 or the logo is not very different from"
                     " the background try to change the", md.bold("sensitivity"), "of the model"),
            md.text("Increasing 📈 the sensitivity will cut off incorrectly found objects, and decreasing 📉 \- "
                      "will draw more attention to objects that similar to the logo"),
            md.text("Sensitivity varies from 0\.05 to 1,", md.bold("default is 0.5")),
            md.text("\nNote that the sensitivity will change for all your following requests ⚠️"),
            md.text(f"\nYour current sensetitvity level \-", md.bold(f"{user.sens_level}"),
            ),
            sep='\n'
        )
    )
    await callback.message.answer(
        text=md.text(
            "Enter a new value for sensitivity from", md.bold("0.05 to 1"), "in increments of", md.bold("0.05"),
            "\nTo undo this operation ↩️ write /cancel command"
        )
    )
    await state.set_state(ChangeSens.changing_sens)


async def sens_chosen(message: Message, state: FSMContext, user: dbm.User):
    try:
        new_sens = float(message.text.lower().strip())
        if new_sens > 1 or new_sens < 0.05:
            await message.answer("The number is out of range\. Please specify number from 0\.05 to 1")
        elif new_sens not in [i / 20 for i in range(21)]:
            await message.answer("The number is not divisible by 0\.05\. Enter a number that will be a multiple of 0\.05")
        else:
            user.update(sens_level=new_sens)
            await message.answer(md.bold("The sensitive level was changed!"))
            await state.clear()
            await get_menu(message)
    except ValueError as e:
        logging.warning(e)
        await message.answer(
            text="Wrong number input\. Value must be in d\.dd format"
        )


async def show_labels_info(callback: CallbackQuery, user: dbm.User):
    text = str()
    if user.show_labels:
        text = "Show labels ✅"
    else:
        text = "Hide labels ❌"
    await callback.message.edit_text(
        text=f"This setting is responsible for displaying the class name and the confidence level on the frame\n"
             f"Current state \- {text}",
        reply_markup=get_show_labels_keyboard()
    )
    await callback.answer()


async def change_labels(callback: CallbackQuery, callback_data: ShowLabelData, user: dbm.User):
    user.update(show_labels=callback_data.value)
    text = str()
    if callback_data.value:
        text = "Show labels ✅"
    else:
        text = "Hide labels ❌"
    await callback.answer(text=f"Showing labels was changed for: {text}")
    await callback.message.edit_text(
        text="This is main menu\. Choose what you want to do:",
        reply_markup=get_main_keyboard()
    )


async def warning_sens(message: Message):
    await message.answer("You need to finish your current action")


async def warning_sens_cl(callback: CallbackQuery):
    await callback.answer(
        text="To run any command you need to stop sending media\n"
             "To do this send /cancel command",
        show_alert=True
    )
