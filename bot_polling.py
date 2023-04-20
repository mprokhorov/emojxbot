import asyncio
import logging

from aiogram import Bot, Dispatcher
from redis.asyncio.client import Redis
from aiogram.fsm.storage.redis import RedisStorage
from config_reader import config
from handlers import new, split, delete


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    redis = Redis(decode_responses=True,
                  host=config.redis_host.get_secret_value(),
                  port=config.redis_port.get_secret_value(),
                  username=config.redis_username.get_secret_value(),
                  password=config.redis_password.get_secret_value())
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_routers(new.router, split.router, delete.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
