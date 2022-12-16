from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError, CantInitiateConversation

from locales import Locale


async def errors_handler(update: types.Update, exception: TelegramAPIError):
    if isinstance(exception, CantInitiateConversation):
        await update.callback_query.message.reply(Locale.Error.UNABLE_TO_INITIALIZE_CHAT, disable_notification=True)
        return True
