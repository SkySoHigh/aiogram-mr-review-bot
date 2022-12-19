from typing import Union

from aiogram import types

from common import app
from keyboard.keyboards import get_tasks_on_review_menu, get_tasks_confirmation_menu, get_tasks_submitted_menu
from locales import Locale
from utils import get_current_datetime

from views import generate_task_view, get_id_from_view_text


async def publish_task_for_review(message: types.Message):
    if len(message.text.split(' ', 1)) != 2:
        await message.reply(text=Locale.Error.INCORRECT_REVIEW_SUBMIT_COMMAND,
                            disable_notification=True,
                            disable_web_page_preview=True,
                            )
    else:
        task_id = app.task_service.create_task(url=message.text.strip().split(' ', 1)[1],
                                               chat_id=message.chat.id,
                                               publisher_msg_id=message.message_id,
                                               publisher_id=message.from_user.id,
                                               publisher_name=message.from_user.username,
                                               published_at=message.date,
                                               )
        task = app.task_service.get_task_by_id(task_id=task_id)
        await message.reply(text=generate_task_view(task),
                            reply_markup=get_tasks_on_review_menu(),
                            disable_notification=True,
                            disable_web_page_preview=True,
                            )


async def take_task_on_review_cb(query: types.CallbackQuery):
    await query.answer()
    task_id = get_id_from_view_text(message=query.message.text)
    app.task_service.set_task_reviewer(task_id=task_id,
                                       reviewer_id=query.from_user.id,
                                       reviewer_name=query.from_user.username,
                                       reply_msg_id=query.message.message_id,
                                       taken_on_review_at=get_current_datetime(),
                                       )

    task = app.task_service.get_task_by_id(task_id=task_id)

    await app.bot.edit_message_text(
        text=generate_task_view(task),
        chat_id=task.chat_id,
        message_id=task.reply_msg_id,
        reply_markup=get_tasks_submitted_menu(),
        disable_web_page_preview=True,
    )


async def submit_reviewed_task_cb(query: types.CallbackQuery):
    await query.answer()
    task_id = get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if query.from_user.id in [task.reviewer_id, *app.config.common.admins]:
        app.task_service.submit_task_to_final_review(task_id=task_id,
                                                     submitted_to_final_review_at=get_current_datetime(),
                                                     )
        await update_view_with_db_data(task_id=task_id, query=query, reply_markup=get_tasks_confirmation_menu())
    else:
        await query.message.reply(text=Locale.Error.UNABLE_TO_SUBMIT_TASK_BY_ANY_USER)


async def confirm_reviewed_task_cb(query: types.CallbackQuery):
    await query.answer()
    task_id = get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if query.from_user.id in [task.reviewer_id, *app.config.common.admins]:

        app.task_service.complete_task_review(task_id=task_id,
                                              final_reviewer_name=query.from_user.username,
                                              completed_at=get_current_datetime(),
                                              )
        await update_view_with_db_data(task_id=task_id, query=query)
    else:
        await query.message.reply(text=Locale.Error.UNABLE_TO_CONFIRM_TASK_BY_ANY_USER)


async def reject_reviewed_task(query: types.CallbackQuery):
    await query.answer()
    task_id = get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if query.from_user.id in [task.reviewer_id, *app.config.common.admins]:
        app.task_service.reject_task_review(task_id=task_id)
        await update_view_with_db_data(task_id=task_id, query=query, reply_markup=get_tasks_submitted_menu())
    else:
        await query.message.reply(text=Locale.Error.UNABLE_REJECT_TASK_BY_ANY_USER)


async def send_user_tasks_on_review_to_pm(query: types.CallbackQuery):
    await send_tasks_on_review_to_reviewer(query=query)


async def send_all_tasks_on_review_to_chat(query: types.CallbackQuery):
    await send_tasks_on_review_to_reviewer(query=query, to_group_chat=True)


async def send_tasks_on_review_to_reviewer(query: types.CallbackQuery, *, to_group_chat: bool = False):
    if to_group_chat:
        tasks = app.task_service.get_all_tasks_on_review(chat_id=query.message.chat.id)
    else:
        tasks = app.task_service.get_all_tasks_on_review(chat_id=query.message.chat.id, reviewer_id=query.from_user.id)

    header_msg = f'{Locale.Common.CHAT_ORIGIN_MSG} {query.message.chat.title}'

    if not tasks:
        await app.bot.send_message(chat_id=query.from_user.id,
                                   text=f'{header_msg}\n'
                                        f'{Locale.Task.NO_TASKS_MSG}')
    else:
        sent_tasks = 0
        for t in tasks:
            if sent_tasks == app.config.common.task_limit:
                tasks_count = app.task_service.count_tasks_on_review(query.message.chat.id)
                await app.bot.send_message(text=f'{Locale.Error.TO_MANY_UNFINISHED_TASKS}: {tasks_count}\n'
                                                f'{Locale.Task.TASK_LIMIT_IS}: {app.config.common.task_limit}',
                                           chat_id=t.chat_id,
                                           disable_notification=True)
                break

            await app.bot.send_message(
                text=f'{header_msg}\n'
                     f'{generate_task_view(t)}',
                chat_id=t.chat_id,
                reply_markup=get_tasks_confirmation_menu()
                if t.submitted_to_final_review_at else get_tasks_submitted_menu(),
                disable_web_page_preview=True,
            )

            sent_tasks += 1


async def update_view_with_db_data(task_id: int, query: types.CallbackQuery,
                                   reply_markup: Union[types.InlineKeyboardMarkup, None] = None):
    task = app.task_service.get_task_by_id(task_id=task_id)
    await app.bot.edit_message_text(text=generate_task_view(task),
                                    chat_id=task.chat_id,
                                    message_id=task.reply_msg_id,
                                    reply_markup=reply_markup,
                                    disable_web_page_preview=True,
                                    )
    # If msg edited from private message -> update origin (chat from which task came from) OR ...
    # If it is private user's chat with bot -> update origin (chat from which task came from -> this chat)
    if (task.chat_id != query.message.chat.id) or (task.reviewer_id == query.message.chat.id):
        await app.bot.edit_message_text(text=generate_task_view(task),
                                        chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        reply_markup=reply_markup,
                                        disable_web_page_preview=True,
                                        )
