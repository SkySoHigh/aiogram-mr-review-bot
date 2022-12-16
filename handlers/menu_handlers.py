from aiogram import types

from common import app
from keyboard.keyboards import get_main_menu

from locales import Locale


async def show_main_menu(message: types.Message):
    await message.reply(Locale.Menu.MENU_HEADER, reply_markup=get_main_menu(), disable_notification=True)


async def show_all_user_tasks(callback_query: types.CallbackQuery):
    await app.bot.send_message(chat_id=callback_query.from_user.id, text="тут бидуn заПИСЬКИ...")
    await callback_query.message.reply(Locale.Menu.SHOW_TASKS_BTN_CONFIRMED_MSG, disable_notification=True)


async def show_adm_menu(callback_query: types.CallbackQuery):
    await callback_query.message.reply(Locale.Menu.SHOW_ADM_MENU_BTN_CONFIRMED_MSG, disable_notification=True)
    await app.bot.send_message(chat_id=callback_query.from_user.id, text="тут бидуте админское меню")
