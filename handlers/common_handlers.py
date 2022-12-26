from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart

from loader import dp
from locales import Locale


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Handler for bot start
    :param message: Message received by the bot from the user
    :return:
    """
    await message.reply(Locale.Common.GREETING_MSG)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.reply(Locale.Common.HELP_MSG)
