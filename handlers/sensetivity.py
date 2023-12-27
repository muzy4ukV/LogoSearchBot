import logging

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from states import ChangeSens
import markdown as md
from database import models as dbm


async def change_sens(message: Message, state: FSMContext, user: dbm.User):
    await message.answer(
        text=md.text(
            md.quote("If the quality of your photo is not high, or the logo is not very different from"
                     " the background, we recommend to change the sensitivity of the model"),
            md.italic("Increasing the sensitivity will cut off incorrectly found objects, and decreasing it - "
                      "will draw more attention to objects that similar to the logo"),
            md.text("Sensitivity varies from 0\.05 to 1,", md.bold("default is 0.5")),
            md.text("\nNote that the sensitivity will change for all your following requests"),
            md.text(f"Your current sensetitvity \-", md.bold(f"{user.sens_level}"),
            ),
            sep = '\n'
        )
    )
    await message.answer(
        text=md.text(
            "Enter a new value for sensitivity from 0\.05 to 1 in increments of 0\.05\n"
            "To undo it write", md.bold("/cancel"), "command"
        )
    )
    await state.set_state(ChangeSens.changing_new_sens)


async def sens_chosen(message: Message, state: FSMContext, user: dbm.User):
    try:
        new_sens = float(message.text.lower().strip())
        if new_sens > 1 or new_sens < 0.05:
            await message.answer("The number is out of range\. Please specify number from 0\.05 to 1")
        elif new_sens not in [i / 20 for i in range(21)]:
            await message.answer("The number is not divisible by 0\.05\. Enter a number that will be a multiple of 0\.05")
        else:
            user.update(sens_level=new_sens)
            await message.answer("The sensitive level was changed\!")
            await state.clear()
    except ValueError as e:
        logging.warning(e)
        await message.answer(
            text="Wrong number input\. Value must be in d\.dd format"
        )


async def warning_sens(message: Message):
    await message.answer("You need to finish your current action")