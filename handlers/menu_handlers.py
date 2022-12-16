from aiogram import types

from common import app
from db.models.tasks import TaskStates
from keyboard.keyboards import get_main_menu, get_tasks_submitted_menu

from locales import Locale


async def show_main_menu(message: types.Message):
    await message.reply(Locale.Menu.MENU_HEADER, reply_markup=get_main_menu(), disable_notification=True)


async def show_all_user_tasks(query: types.CallbackQuery):
    tasks = app.db_client.tasks.read_by(origin_chat=query.message.chat.id, applicant=query.from_user.id,
                                        status=TaskStates.ON_REVIEW, limit=app.config.common.task_limit)

    await query.message.reply(text=f'{Locale.Menu.SHOW_TASKS_LIMIT_MSG} {app.config.common.task_limit} \n'
                                   f'{Locale.Menu.SHOW_TASKS_CONFIRMED_MSG}', disable_notification=True)

    reviewer = await app.bot.get_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
    await app.bot.send_message(chat_id=reviewer.user.id,
                               text=f'{Locale.Common.CHAT_ORIGIN_MSG} {query.message.chat.title}')
    if not tasks:
        await app.bot.send_message(chat_id=reviewer.user.id, text=f'{Locale.NewTaskOnReview.NO_TASKS_MSG}')
    else:
        for t in tasks:

            await app.bot.send_message(
                text=f'{Locale.TaskSubmitted.SUBMITTED_MSG_ACCEPTED_TIME} {t.acceptance_time}\n'
                     f'{Locale.TaskSubmitted.SUBMITTED_MSG_ACCEPTED_BY} {reviewer.user.first_name} {reviewer.user.last_name}\n'
                     f'-> {t.id}',
                chat_id=reviewer.user.id,
                reply_markup=get_tasks_submitted_menu())


async def show_adm_menu(callback_query: types.CallbackQuery):
    await callback_query.message.reply(Locale.Menu.SHOW_ADM_MENU_BTN_CONFIRMED_MSG, disable_notification=True)
    await app.bot.send_message(chat_id=callback_query.from_user.id, text="тут бидуте админское меню")
