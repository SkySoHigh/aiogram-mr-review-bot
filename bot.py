from aiogram import executor, Dispatcher

import filters
import handlers
from common import set_default_commands
from common import app


async def on_startup(dp: Dispatcher):
    filters.setup(dp)
    handlers.setup(dp)
    await set_default_commands(dp)


async def on_shutdown(dp: Dispatcher):
    ...


if __name__ == '__main__':
    executor.start_polling(app.dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
