import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from sqlalchemy.engine import URL

from config import config
from routers import new, split, delete

from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas


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

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username="postgres",
        host="localhost",
        port=5432,
        database="postgres",
        password="547244"
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
