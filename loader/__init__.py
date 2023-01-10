from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from common import commands
from configs.configs import ConfigProvider
from loader.initializer import Loader
from locales.RuLocale import RuLocale
from utils import logger

__all__ = ["app", "dp", "bot", "run", "Locale", "config"]

Locale = RuLocale

config = ConfigProvider()
bot = Bot(token=config.common.token.get_secret_value())
dp = Dispatcher(bot, storage=MemoryStorage())
app = Loader(config=config, bot=bot, dp=dp)
logger.setup_logging(logging_cfg_path=config.common.log_cfg_path)


async def on_startup(dp: Dispatcher):
    # Setup custom filters
    import filters

    filters.setup(dp)

    # Setup database
    app.init_db()

    # Register bot commands
    await commands.set_default_commands(dp)

    import handlers.common_handlers  # noqa
    import handlers.error_handlers  # noqa
    import handlers.menu_handlers  # noqa
    import handlers.task_handlers  # noqa

    # Add middleware
    from middleware.antiflood import ThrottlingMiddleware

    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())


async def on_shutdown(dp: Dispatcher):
    ...


def run():
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
