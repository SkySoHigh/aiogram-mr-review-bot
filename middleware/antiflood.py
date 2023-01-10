import asyncio
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from handlers.error_handlers import show_error_msg_for_n_seconds
from loader import Locale, config


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=config.common.throttling_limit, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def process(self, msg: Union[types.CallbackQuery, types.Message], data: dict):
        msg = msg if isinstance(msg, types.Message) else msg.message
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(
                handler, "throttling_key", f"{self.prefix}_{handler.__name__}"
            )
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(msg, t)

            # Cancel current handler
            raise CancelHandler()

    async def on_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.process(query, data)

    async def on_process_message(self, message: types.Message, data: dict):
        await self.process(message, data)

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await show_error_msg_for_n_seconds(
                message, error_msg=f"{Locale.Error.THROTTLING_WARN} {throttled.rate}s"
            )
        await asyncio.sleep(delta)
