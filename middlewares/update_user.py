from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, types

from database import models as dbm
import os


class UpdateUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[types.Message, types.CallbackQuery],
        data: Dict[str, Any]
    ):
        user: dbm.User = dbm.User.get_pk(event.from_user.id)

        if user and event.from_user.username != user.username:
            user = user.update(username=event.from_user.username)
        elif not user:
            data_folder = f"users/{event.from_user.id}/data"
            result_folder = f"users/{event.from_user.id}/result"
            if not os.path.exists(f"users/{event.from_user.id}"):
                os.makedirs(data_folder, exist_ok=True)
                os.mkdir(result_folder)
            user = dbm.User.add_new(
                user_id=event.from_user.id,
                username=event.from_user.username,
                data_folder=data_folder,
                result_folder=result_folder
            )

        data['user'] = user
        return await handler(event, data)
