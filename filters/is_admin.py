from typing import Union, List

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    ADMIN_IDS: List[int] = []  # Should be set before binding to bot

    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, obj: Union[types.Message, types.CallbackQuery]):
        user = obj.from_user
        if user.id in AdminFilter.ADMIN_IDS:
            return self.is_admin is True
        return self.is_admin is False
