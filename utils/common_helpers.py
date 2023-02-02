import re
from typing import List

import aiogram.bot.bot

from loader import Locale


def generate_link_to_msg(chat_id: int, msg_id: int) -> str:
    shift = -1_000_000_000_000
    return f"https://t.me/c/{shift - chat_id}/{msg_id}"


def get_id_from_view_text(message: str) -> int:
    try:
        return re.findall(pattern=Locale.Task.ID + ":\s(\\d+)", string=message)[0]
    except KeyError:
        raise KeyError  # !TODO raise normal exception


async def get_chat_admins(
    bot: aiogram.bot.bot.Bot, chat_id: int, exclude_bots: bool = True
) -> List[int]:
    chat_admins = []
    for adm in await bot.get_chat_administrators(chat_id=chat_id):
        if adm.user.is_bot is True and exclude_bots is True:
            continue
        chat_admins.append(adm.user.id)
    return chat_admins
