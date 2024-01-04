from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, types

from database import models as dbm
import os
import mmh3


class UpdateUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[types.Message, types.CallbackQuery],
        data: Dict[str, Any]
    ):

        hashed_value = mmh3.hash(str(event.from_user.id), 42)

        user: dbm.User = dbm.User.get_pk(hashed_value)

        if user and event.from_user.username != user.username:
            user = user.update(username=event.from_user.username)
        elif not user:
            data_folder = f"users/{hashed_value}/data"
            result_folder = f"users/{hashed_value}/result"
            if not os.path.exists(f"users/{hashed_value}"):
                os.makedirs(data_folder, exist_ok=True)
                os.mkdir(result_folder)
            user = dbm.User.add_new(
                hash_id=hashed_value,
                user_id=event.from_user.id,
                username=event.from_user.username,
                data_folder=data_folder,
                result_folder=result_folder
            )

        data['user'] = user
        return await handler(event, data)
