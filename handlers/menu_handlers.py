from aiogram import types

from common import app
from keyboard.keyboards import get_main_menu
from locales import Locale


async def show_main_menu(message: types.Message):
    await message.reply(text=Locale.Menu.MENU_HEADER,
                        reply_markup=get_main_menu(),
                        disable_notification=True,
                        )


async def show_adm_menu(callback_query: types.CallbackQuery):
    await app.bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'{Locale.Common.CHAT_ORIGIN_MSG}\n'
                                    f'Admins menu',
                               disable_notification=True,
                               )
