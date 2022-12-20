from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from loader import dp
from locales import Locale


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.reply(Locale.Common.GREETING_MSG)


@dp.message_handler(CommandHelp())
async def help(message: types.Message):
    await message.reply(Locale.Common.HELP_MSG)
