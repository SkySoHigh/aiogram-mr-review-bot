import asyncio
from datetime import datetime

from aiogram import types

from loader import app, dp


async def periodic_reminder(sleep_for=5):
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.utcnow()
        await app.bot.send_message(340541141, f"{now}")


async def set_global_reminder(message: types.Message):
    if not app.periodic_task:
        await message.reply("There is no background task. Creating")
        app.periodic_task = asyncio.ensure_future(periodic_reminder())


async def unset_global_reminder(message: types.Message):
    if not app.periodic_task:
        await message.reply("There is no background task. Creating")
        app.periodic_task = asyncio.ensure_future(periodic_reminder())
