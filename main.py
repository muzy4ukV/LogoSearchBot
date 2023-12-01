import asyncio
from aiogram import Bot, Dispatcher
import logging
from settings import settings
from routers import files_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())

    dp = Dispatcher()
    dp.include_router(files_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())