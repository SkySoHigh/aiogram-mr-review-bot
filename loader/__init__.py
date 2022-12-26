from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from common import commands
from configs.configs import ConfigProvider
from locales.RuLocale import RuLocale
from utils import logger
from loader.initializer import Loader

__all__ = ["app", "dp", "bot", "run", "Locale"]

Locale = RuLocale

config = ConfigProvider()
bot = Bot(token=config.common.token.get_secret_value())
dp = Dispatcher(bot)
app = Loader(config=config, bot=bot, dp=dp)
logger.setup_logging(logging_cfg_path=config.common.log_cfg_path)


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
    import handlers  # noqa


async def on_shutdown(dp: Dispatcher):
    ...


def run():
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
