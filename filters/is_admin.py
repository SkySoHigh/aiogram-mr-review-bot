from typing import Union, List

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from common import app


class AdminFilter(BoundFilter):

    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, obj: Union[types.Message, types.CallbackQuery]):
        user = obj.from_user
        if user.id in app.config.common.admins:
            return self.is_admin is True
        return self.is_admin is False
