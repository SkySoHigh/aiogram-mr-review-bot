from aiogram import types

from locales import Locale


async def start(message: types.Message):
    await message.reply(Locale.Common.GREETING_MSG)


async def help(message: types.Message):
    await message.reply(Locale.Common.HELP_MSG)
