from aiogram.fsm.state import StatesGroup, State


class MediaProcessing(StatesGroup):
    sending_media = State()
    running_model = State()


class ChangeSens(StatesGroup):
    changing_sens = State()


