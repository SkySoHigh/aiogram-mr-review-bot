from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError, CantInitiateConversation, MessageToForwardNotFound, MessageToEditNotFound

from locales import Locale


async def errors_handler(update: types.Update, exception: TelegramAPIError):
    if isinstance(exception, CantInitiateConversation):
        await update.callback_query.message.reply(Locale.Error.UNABLE_TO_INITIALIZE_CHAT, disable_notification=True)
        return True

    if isinstance(exception, MessageToForwardNotFound):
        await update.callback_query.message.reply(f'{Locale.Error.MESSAGE_FORWARD_NOT_FOUND}\n'
                                                  f'{Locale.Error.CONTACT_ADMINISTRATOR}', disable_notification=True)
        return True

    if isinstance(exception, MessageToEditNotFound):
        await update.callback_query.message.reply(f'{Locale.Error.MESSAGE_TO_EDIT_NOT_FOUND}\n'
                                                  f'{Locale.Error.CONTACT_ADMINISTRATOR}', disable_notification=True)
        return True
