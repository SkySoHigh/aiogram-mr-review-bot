from dataclasses import dataclass
from typing import Union, List

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatType

from loader import app


# TODO: There is a bug, when filter check is called for every usage in cb. Gonna use method instead.

@dataclass
class AdminFilter(BoundFilter):
    key = "is_admin"
    is_admin: bool

    async def check(self, obj: Union[types.Message, types.CallbackQuery]):
        user = obj.from_user
        chat_admins = []

        # If chat is private we will not be able to get admins
        if obj.message.chat.type != ChatType.PRIVATE:
            chat_admins.extend([a.user.id for a in await obj.bot.get_chat_administrators(chat_id=obj.message.chat.id)])
        else:
            chat_admins.append(obj.from_user.id)
        print('AAAA')
        if user.id in [app.config.common.admins, *chat_admins]:
            return self.is_admin is True
        else:
            # await self.handle_no_rights_error(obj)
            return self.is_admin is False


async def check(obj: Union[types.Message, types.CallbackQuery], *, additional_ids: List[int] = None) -> bool:
    user = obj.from_user
    additional_ids = additional_ids if additional_ids else []
    chat_admins = []

    chat_admins.extend(additional_ids)

    # If chat is private we will not be able to get admins
    if obj.message.chat.type != ChatType.PRIVATE:
        chat_admins.extend([a.user.id for a in await obj.bot.get_chat_administrators(chat_id=obj.message.chat.id)])
    else:
        chat_admins.append(obj.from_user.id)
    if user.id in [app.config.common.admins, *chat_admins]:
        return True
    else:
        return False
