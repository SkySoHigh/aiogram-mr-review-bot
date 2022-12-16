from aiogram import types

from locales import Locale


async def start(message: types.Message):
    await message.reply(Locale.StartUp.GREETING_MSG)


async def help(message: types.Message):
    await message.reply(Locale.StartUp.HELP_MSG)
