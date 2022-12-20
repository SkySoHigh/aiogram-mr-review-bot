from typing import Union

from aiogram import types

from common import callbacks
from common import commands
from common import keyboards
from filters import is_admin
from handlers.error_handlers import show_error_msg_for_n_seconds
from loader import app, dp
from locales import Locale
from utils import get_current_datetime
from views import generate_task_view, get_id_from_view_text


@dp.message_handler(commands.CommandPublishReview())
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
                            reply_markup=keyboards.get_tasks_on_review_menu(),
                            disable_notification=True,
                            disable_web_page_preview=True,
                            )


@dp.callback_query_handler(callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuOnReview.take))
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

    await query.bot.edit_message_text(
        text=generate_task_view(task),
        chat_id=task.chat_id,
        message_id=task.reply_msg_id,
        reply_markup=keyboards.get_tasks_submitted_menu(),
        disable_web_page_preview=True,
    )


@dp.callback_query_handler(callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuFinalReview.submitted))
async def submit_reviewed_task_cb(query: types.CallbackQuery):
    await query.answer()
    task_id = get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if await is_admin.check(obj=query, additional_ids=[task.reviewer_id]):
        app.task_service.submit_task_to_final_review(task_id=task_id,
                                                     submitted_to_final_review_at=get_current_datetime(),
                                                     )
        await update_view_with_db_data(task_id=task_id, query=query,
                                       reply_markup=keyboards.get_tasks_confirmation_menu())
    else:
        await show_error_msg_for_n_seconds(obj=query, error_msg=Locale.Error.UNABLE_TO_SUBMIT_TASK_BY_ANY_USER)


@dp.callback_query_handler(callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuReviewFinished.confirmed))
async def confirm_reviewed_task_cb(query: types.CallbackQuery):
    if await is_admin.check(obj=query):
        await query.answer()
        task_id = get_id_from_view_text(message=query.message.text)
        app.task_service.complete_task_review(task_id=task_id,
                                              final_reviewer_name=query.from_user.username,
                                              completed_at=get_current_datetime(),
                                              )
        await update_view_with_db_data(task_id=task_id,
                                       query=query,
                                       )
    else:
        await show_error_msg_for_n_seconds(obj=query, error_msg=Locale.Error.ADMIN_RIGHTS_REQUIRED)


@dp.callback_query_handler(callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuReviewFinished.rejected))
async def reject_reviewed_task(query: types.CallbackQuery):
    if await is_admin.check(obj=query):
        await query.answer()
        task_id = get_id_from_view_text(message=query.message.text)
        app.task_service.reject_task_review(task_id=task_id)
        await update_view_with_db_data(task_id=task_id,
                                       query=query,
                                       reply_markup=keyboards.get_tasks_submitted_menu(),
                                       )
    else:
        await show_error_msg_for_n_seconds(obj=query, error_msg=Locale.Error.ADMIN_RIGHTS_REQUIRED)


@dp.callback_query_handler(callbacks.MenuCallBack.filter(action=keyboards.MainMenu.send_tasks_to_pm))
async def send_user_tasks_on_review_to_pm(query: types.CallbackQuery):
    await send_users_tasks_on_review_to_pm(query=query)


@dp.callback_query_handler(callbacks.MenuCallBack.filter(action=keyboards.MainMenu.send_tasks_to_group_chat))
async def send_all_tasks_on_review_to_chat(query: types.CallbackQuery):
    await send_tasks_on_review_to_chat(query=query)


async def send_users_tasks_on_review_to_pm(query: types.CallbackQuery, ):
    tasks = app.task_service.get_all_tasks_on_review(chat_id=query.message.chat.id, reviewer_id=query.from_user.id)
    header_msg = f'{Locale.Common.CHAT_ORIGIN_MSG} {query.message.chat.title}'

    if not tasks:
        await query.bot.send_message(chat_id=query.from_user.id,
                                     text=f'{header_msg}\n'
                                          f'{Locale.Task.NO_TASKS_MSG}')
        return

    sent_tasks = 0
    for t in tasks:
        if sent_tasks == app.config.common.task_limit:
            tasks_count = app.task_service.count_tasks_on_review(query.message.chat.id)
            await query.bot.send_message(text=f'{Locale.Error.TO_MANY_UNFINISHED_TASKS}: {tasks_count}\n'
                                              f'{Locale.Task.TASK_LIMIT_IS}: {app.config.common.task_limit}',
                                         chat_id=t.reviewer_id,
                                         disable_notification=True)
            break

        # await query.bot.forward_message(chat_id=t.reviewer_id,
        #                                 from_chat_id=t.chat_id,
        #                                 message_id=t.reply_msg_id, )
        await query.bot.send_message(
            text=f'{header_msg}\n'
                 f'{generate_task_view(t)}',
            chat_id=t.reviewer_id,
            disable_web_page_preview=True,
        )
        sent_tasks += 1


async def send_tasks_on_review_to_chat(query: types.CallbackQuery):
    tasks = app.task_service.get_all_tasks_on_review(chat_id=query.message.chat.id, reviewer_id=query.from_user.id)
    header_msg = f'{Locale.Common.CHAT_ORIGIN_MSG} {query.message.chat.title}'

    if not tasks:
        await query.bot.send_message(chat_id=query.message.chat.id,
                                     text=f'{header_msg}\n'
                                          f'{Locale.Task.NO_TASKS_MSG}')
        return

    sent_tasks = 0
    task_to_reply_msg_id = []  # (task id | new reply msg | old reply msg )
    for t in tasks:
        if sent_tasks == app.config.common.task_limit:
            tasks_count = app.task_service.count_tasks_on_review(query.message.chat.id)
            await query.bot.send_message(text=f'{Locale.Error.TO_MANY_UNFINISHED_TASKS}: {tasks_count}\n'
                                              f'{Locale.Task.TASK_LIMIT_IS}: {app.config.common.task_limit}',
                                         chat_id=t.chat_id,
                                         disable_notification=True)
            break

        msg = await query.bot.send_message(
            text=f'{header_msg}\n'
                 f'{generate_task_view(t)}',
            chat_id=t.chat_id,
            reply_markup=keyboards.get_tasks_confirmation_menu() if t.submitted_to_final_review_at
            else keyboards.get_tasks_submitted_menu(),
            disable_web_page_preview=True,
        )
        task_to_reply_msg_id.append((t.id, msg.message_id, t.reply_msg_id))

        sent_tasks += 1

    for u in task_to_reply_msg_id:
        app.task_service.set_reply_msg_id(u[0], u[1])
        await query.bot.delete_message(query.message.chat.id, u[2])


async def update_view_with_db_data(task_id: int, query: types.CallbackQuery,
                                   reply_markup: Union[types.InlineKeyboardMarkup, None] = None):
    task = app.task_service.get_task_by_id(task_id=task_id)
    await query.bot.edit_message_text(text=generate_task_view(task),
                                      chat_id=task.chat_id,
                                      message_id=task.reply_msg_id,
                                      reply_markup=reply_markup,
                                      disable_web_page_preview=True,
                                      )
    # If msg edited from private message -> update origin (chat from which task came from) OR ...
    # If it is private user's chat with bot -> update origin (chat from which task came from -> this chat)
    # if task.reply_msg_id != query.message.message_id:
    #     await app.bot.edit_message_text(text=generate_task_view(task),
    #                                     chat_id=query.message.chat.id,
    #                                     message_id=query.message.message_id,
    #                                     reply_markup=reply_markup,
    #                                     disable_web_page_preview=True,
    #                                     )
