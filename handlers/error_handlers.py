import asyncio
from typing import Union

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError, CantInitiateConversation, MessageToForwardNotFound, \
    MessageToEditNotFound

from loader import dp
from locales import Locale


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: TelegramAPIError):
    if isinstance(exception, CantInitiateConversation):
        await show_error_msg_for_n_seconds(update.callback_query, Locale.Error.UNABLE_TO_INITIALIZE_CHAT)
        return True

    if isinstance(exception, MessageToForwardNotFound):
        await show_error_msg_for_n_seconds(update.callback_query,
            f'{Locale.Error.MESSAGE_FORWARD_NOT_FOUND}\n'
                                           f'{Locale.Error.CONTACT_ADMINISTRATOR}')
        return True

    if isinstance(exception, MessageToEditNotFound):
        await show_error_msg_for_n_seconds(update.callback_query,
                                           f'{Locale.Error.MESSAGE_TO_EDIT_NOT_FOUND}\n'
                                           f'{Locale.Error.CONTACT_ADMINISTRATOR}')

        return True


async def show_error_msg_for_n_seconds(obj: Union[types.Message, types.CallbackQuery], error_msg: str,
                                       duration: int = 10):
    msg_for_removal = await obj.bot.send_message(text=f'{error_msg}\n'
                                                      f'{Locale.Error.ERROR_MSG_WILL_BE_REMOVED_IN}: {duration}s',
                                                 chat_id=obj.message.chat.id,
                                                 disable_notification=True,
                                                 disable_web_page_preview=True,
                                                 )
    await asyncio.sleep(duration)
    await obj.bot.delete_message(chat_id=msg_for_removal.chat.id, message_id=msg_for_removal.message_id)
