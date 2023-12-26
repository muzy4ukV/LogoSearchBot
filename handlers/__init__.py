from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import default_state

from states import MediaProcessing, ChangeSens

from .start import start_message
from .photo import get_photo, get_file_photo
from .result import return_result, warning_send_media
from .canceling import cmd_cancel, cmd_cancel_no_state, cmd_cancel_sending_media

import os

default_router = Router()

default_router.message.register(start_message, CommandStart())
default_router.message.register(get_photo, MediaProcessing.sending_media, F.photo)
default_router.message.register(get_file_photo, MediaProcessing.sending_media, F.document)
default_router.message.register(return_result, MediaProcessing.sending_media, Command("run"))

default_router.message.register(warning_send_media, Command("run"))
default_router.message.register(cmd_cancel_no_state, default_state, Command("cancel"))
default_router.message.register(cmd_cancel_sending_media, MediaProcessing.sending_media, Command("cancel"))
default_router.message.register(cmd_cancel, Command("cancel"))

