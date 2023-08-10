import logging

from aiogram import Dispatcher, Router, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application
from redis.asyncio.client import Redis

from config import config
from routers import new, split, delete, forwarded, add, test
from ui_commands import set_ui_commands

WEBHOOK_HOST = config.webhook_host.get_secret_value()
WEBHOOK_PATH = config.webhook_path.get_secret_value()
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = config.webapp_host.get_secret_value()
WEBAPP_PORT = config.webapp_port.get_secret_value()

router = Router()


@router.startup()
async def on_startup(bot: Bot, webhook_url: str):
    await bot.set_webhook(webhook_url)


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


def main():
    redis = Redis(decode_responses=True,
                  host=config.redis_host.get_secret_value(),
                  port=config.redis_port.get_secret_value(),
                  username=config.redis_username.get_secret_value(),
                  password=config.redis_password.get_secret_value())

    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))
    dispatcher['webhook_url'] = WEBHOOK_URL
    dispatcher.include_routers(router, new.router, split.router, delete.router,
                               forwarded.router, add.router, test.router)
    # set_ui_commands(bot)
    app = Application()
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)
    setup_application(app, dispatcher, bot=bot)
    run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
