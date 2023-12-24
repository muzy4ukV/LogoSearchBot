from aiogram.fsm.state import StatesGroup, State


class MediaProcessing(StatesGroup):
    sending_media = State()
    processing_media = State()


class ChangeSens(StatesGroup):
    changing_new_sens = State()


