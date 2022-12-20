import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from common import commands
from configs import ConfigProvider
from .loader import Loader

__all__ = ['app', 'dp', 'bot']

config = ConfigProvider()
bot = Bot(token=config.common.token.get_secret_value())
dp = Dispatcher(bot)
app = Loader(config=config, bot=bot, dp=dp)

logging.basicConfig(level=logging.DEBUG)

async def on_startup(dp: Dispatcher):
    # Setup custom filters
    import filters
    filters.setup(dp)

    # Setup database
    app.init_db()

    # Add middleware
    dp.middleware.setup(LoggingMiddleware())

    # Register bot commands
    await commands.set_default_commands(dp)

    # noinspection PyUnresolvedReferences
    import handlers


async def on_shutdown(dp: Dispatcher):
    ...


def run():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
