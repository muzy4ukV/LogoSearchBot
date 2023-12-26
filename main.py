import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from settings import settings

from handlers import default_router
from middlewares.update_user import UpdateUserMiddleware


async def on_startup(bot: Bot):
    default_commands = [
        BotCommand(
            command='start',
            description='Send your media'
        ),
        BotCommand(
            command='run',
            description='Start detecting model'
        ),
        BotCommand(
            command='last_result',
            description='Get last detection result'
        ),
        BotCommand(
            command='change_sens',
            description='Change a sensetivity of model'
        ),
        BotCommand(
            command='cancel',
            description='Cancel current action'
        )
    ]

    await bot.set_my_commands(
        commands=default_commands,
        scope=BotCommandScopeDefault()
    )


async def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.MARKDOWN_V2)

    dp = Dispatcher()
    dp.include_routers(
        default_router
    )
    dp.startup.register(on_startup)

    dp.message.middleware(UpdateUserMiddleware())
    dp.callback_query.middleware(UpdateUserMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.warning("LogoSearchBot")

    asyncio.run(main())