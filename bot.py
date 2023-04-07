import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
from config_reader import config
from handlers import new, split


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    redis = Redis(decode_responses=True)
    bot = Bot(token=config.bot_token.get_secret_value())
    # dp = Dispatcher()
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_routers(new.router, split.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
