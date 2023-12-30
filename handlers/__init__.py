from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import default_state

from states import MediaProcessing, ChangeSens

from .start import start_message, get_menu
from .downloading import get_photo, get_video, get_document, start_downloading, stop_downloading, get_media_group
from .result import run_model
from .canceling import (cmd_cancel, cancel_no_state, cancel_sending_media,
                        cancel_sens_chosen, no_reply, warning, warning_cl)
from .configuration import (sens_chosen, warning_sens, start_configuration, start_sensitivity,
                            show_labels_info, change_labels, warning_sens_cl)

from callbacks_data import ShowLabelData
from middlewares.albums_collector import AlbumsMiddleware
from settings import settings

default_router = Router()

default_router.message.outer_middleware(AlbumsMiddleware(wait_time_seconds=settings.WAIT_TIME_SETTINGS))

default_router.message.register(start_message, default_state, CommandStart())
default_router.message.register(get_menu, default_state, Command("menu"))

default_router.callback_query.register(start_downloading, default_state, F.data == "download")
default_router.callback_query.register(stop_downloading, MediaProcessing.sending_media, F.data == "stop")

default_router.message.register(get_media_group, MediaProcessing.sending_media, F.media_group_id)
default_router.message.register(get_photo, MediaProcessing.sending_media, F.photo)
default_router.message.register(get_video, MediaProcessing.sending_media, F.video)
default_router.message.register(get_document, MediaProcessing.sending_media, F.document)
default_router.message.register(cancel_sending_media, MediaProcessing.sending_media, Command("cancel"))

default_router.message.register(warning, MediaProcessing.sending_media)
default_router.callback_query.register(warning_cl, MediaProcessing.sending_media)

default_router.callback_query.register(run_model, default_state, F.data == "run")
default_router.callback_query.register(start_configuration, default_state, F.data == "configure")
default_router.callback_query.register(start_sensitivity, default_state, F.data == "sensitivity")

default_router.message.register(cancel_sens_chosen, ChangeSens.changing_sens, Command('cancel'))
default_router.message.register(sens_chosen, ChangeSens.changing_sens, F.text)

default_router.message.register(warning, ChangeSens.changing_sens)
default_router.callback_query.register(warning_cl, ChangeSens.changing_sens)

default_router.callback_query.register(show_labels_info, ShowLabelData.filter(F.action == "show_info"))
default_router.callback_query.register(change_labels, ShowLabelData.filter(F.action == "change"))

default_router.message.register(cancel_no_state, default_state, Command("cancel"))
default_router.message.register(cmd_cancel, Command("cancel"))
default_router.message.register(no_reply)

