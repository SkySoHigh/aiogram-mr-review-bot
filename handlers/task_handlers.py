from typing import Union

from aiogram import types

from common import callbacks, commands, keyboards
from db import TasksModel
from filters import is_admin
from handlers import error_handlers
from loader import Locale, app, dp
from utils import common_helpers, date_helpers
from views import task_view


@dp.message_handler(commands.CommandPublishReview())
async def publish_task_for_review(message: types.Message):
    if len(message.text.split(" ", 1)) != 2:
        await message.reply(
            text=Locale.Error.INCORRECT_REVIEW_SUBMIT_COMMAND,
            disable_notification=True,
            disable_web_page_preview=True,
        )
    else:
        task_id = app.task_service.create_task(
            url=message.text.strip().split(" ", 1)[1],
            chat_id=message.chat.id,
            publisher_msg_id=message.message_id,
            publisher_id=message.from_user.id,
            publisher_name=message.from_user.username,
            published_at=message.date,
        )
        task = app.task_service.get_task_by_id(task_id=task_id)
        await message.reply(
            text=task_view.generate_task_body(task),
            reply_markup=keyboards.get_new_task_menu(),
            disable_notification=True,
            disable_web_page_preview=True,
        )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuOnReview.take.value.cb)
)
async def take_task_on_review(query: types.CallbackQuery):
    await query.answer()
    task_id = common_helpers.get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id)
    if query.from_user.id == task.publisher_id:
        await error_handlers.show_error_msg_for_n_seconds(
            query, Locale.Error.UNABLE_TO_SELF_REVIEW
        )
        return

    task = app.task_service.set_task_reviewer(
        task_id=task_id,
        reviewer_id=query.from_user.id,
        reviewer_name=query.from_user.username,
        reply_msg_id=query.message.message_id,
        taken_on_review_at=date_helpers.get_current_datetime(),
    )
    await query.bot.edit_message_text(
        text=task_view.generate_task_body(task),
        chat_id=task.chat_id,
        message_id=task.reply_msg_id,
        reply_markup=keyboards.get_review_task_menu(),
        disable_web_page_preview=True,
    )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuReview.rejected.value.cb)
)
async def reject_reviewed_task(query: types.CallbackQuery):
    await query.answer()
    task_id = common_helpers.get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if await is_admin.check(obj=query, additional_ids=[task.reviewer_id]):
        task = app.task_service.reject_task_review(
            task_id=task_id,
            rejected_from_final_review_at=date_helpers.get_current_datetime(),
        )
        await update_view_with_table_data(
            task=task, query=query, reply_markup=keyboards.get_task_resubmit_menu()
        )

        # Notify publisher, that review is rejected and fix required
        await query.bot.send_message(
            chat_id=task.publisher_id,
            text=f"{task_view.generate_task_header(query.message.chat.title)}"
            f"{Locale.Task.TASK_FIX_REQUIRED}\n\n"
            f"{task_view.generate_task_body(task)}",
        )

    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query,
            error_msg=Locale.Error.UNABLE_TO_REJECT_TASK_FROM_FINAL_REVIEW_BY_ANY_USER,
        )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuFix.fixed.value.cb)
)
async def resubmit_reviewed_task_cb(query: types.CallbackQuery):
    await query.answer()
    task_id = common_helpers.get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if await is_admin.check(obj=query, additional_ids=[task.publisher_id]):
        task = app.task_service.resubmit_task_to_review_after_fix(task_id=task_id)
        await update_view_with_table_data(
            task=task, query=query, reply_markup=keyboards.get_review_task_menu()
        )

        # Notify reviewer that task is ready for review after fix
        await query.bot.send_message(
            chat_id=task.reviewer_id,
            text=f"{task_view.generate_task_header(query.message.chat.title)}"
            f"{Locale.Task.TASK_IS_READY_REVIEW_AFTER_FIX}\n\n"
            f"{task_view.generate_task_body(task)}",
        )
    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query,
            error_msg=Locale.Error.UNABLE_TO_RESUBMIT_TASK_TO_REVIEW_BY_ANY_USER,
        )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(action=keyboards.TaskMenuReview.submitted.value.cb)
)
async def submit_task_to_final_review(query: types.CallbackQuery):
    await query.answer()
    task_id = common_helpers.get_id_from_view_text(message=query.message.text)
    task = app.task_service.get_task_by_id(task_id=task_id)
    if await is_admin.check(obj=query, additional_ids=[task.reviewer_id]):
        task = app.task_service.submit_task_to_final_review(
            task_id=task_id,
            submitted_to_final_review_at=date_helpers.get_current_datetime(),
        )
        await update_view_with_table_data(
            task=task, query=query, reply_markup=keyboards.get_final_tasks_menu()
        )

        for admin_id in [
            adm.user.id
            for adm in await query.bot.get_chat_administrators(
                chat_id=query.message.chat.id
            )
        ]:
            await query.bot.send_message(
                chat_id=admin_id,
                text=f"{task_view.generate_task_header(query.message.chat.title)}"
                f"{Locale.Task.TASK_IS_READY_FOR_FINAL_REVIEW}\n\n"
                f"{task_view.generate_task_body(task)}",
            )
    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query,
            error_msg=Locale.Error.UNABLE_TO_PASS_TASK_TO_REVIEW_BY_ANY_USER,
        )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(
        action=keyboards.TaskMenuFinalReview.confirmed.value.cb
    )
)
async def accept_final_task_review(query: types.CallbackQuery):
    if await is_admin.check(obj=query):
        await query.answer()
        task_id = common_helpers.get_id_from_view_text(message=query.message.text)
        task = app.task_service.accept_final_task_review(
            task_id=task_id,
            final_reviewer_name=query.from_user.username,
            completed_at=date_helpers.get_current_datetime(),
        )
        await update_view_with_table_data(task=task, query=query)
    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query, error_msg=Locale.Error.ADMIN_RIGHTS_REQUIRED
        )


@dp.callback_query_handler(
    callbacks.ReviewCallBack.filter(
        action=keyboards.TaskMenuFinalReview.rejected.value.cb
    )
)
async def reject_final_task_review(query: types.CallbackQuery):
    if await is_admin.check(obj=query):
        await query.answer()
        task_id = common_helpers.get_id_from_view_text(message=query.message.text)
        task = app.task_service.reject_final_task_review(
            task_id=task_id,
            rejected_from_final_review_at=date_helpers.get_current_datetime(),
        )
        await update_view_with_table_data(
            task=task,
            query=query,
            reply_markup=keyboards.get_review_task_menu(),
        )
        # Notify reviewer and publisher that task is rejected
        await query.bot.send_message(
            chat_id=task.reviewer_id,
            text=f"{Locale.Task.TASK_MR_IS_REJECTED}\n\n"
            f"{task_view.generate_task_body(task)}",
        )
        await query.bot.send_message(
            chat_id=task.publisher_id,
            text=f"{Locale.Task.TASK_MR_IS_REJECTED}\n\n"
            f"{task_view.generate_task_body(task)}",
        )
    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query, error_msg=Locale.Error.ADMIN_RIGHTS_REQUIRED
        )


@dp.callback_query_handler(
    callbacks.MenuCallBack.filter(
        action=keyboards.GroupMainMenu.send_tasks_to_pm.value.cb
    )
)
async def send_user_tasks_on_review_from_this_chat_to_pm(query: types.CallbackQuery):
    await send_users_tasks_on_review_to_pm(query=query)


@dp.callback_query_handler(
    callbacks.MenuCallBack.filter(
        action=keyboards.GroupMainMenu.send_tasks_to_group_chat.value.cb
    )
)
async def send_all_tasks_on_review_from_chat_to_chat(query: types.CallbackQuery):
    await send_chat_users_tasks_on_review_to_chat(query=query)


@dp.callback_query_handler(
    callbacks.MenuCallBack.filter(
        action=keyboards.PmMainMenu.get_all_user_tasks.value.cb
    )
)
async def send_all_tasks_on_review_from_all_chats_to_pm(query: types.CallbackQuery):
    await send_users_tasks_on_review_to_pm(query=query, from_all_chats=True)


async def send_users_tasks_on_review_to_pm(
    query: types.CallbackQuery, from_all_chats: bool = False
):
    chats = []
    if from_all_chats is False:
        chats.append(query.message.chat.id)
    else:
        chats.extend(app.task_service.get_all_reviewer_chats_ids(query.from_user.id))

    if not chats:
        await query.bot.send_message(
            chat_id=query.from_user.id,
            text=f'{task_view.generate_task_header("-")}' f"{Locale.Task.NO_TASKS_MSG}",
        )

    for chat_id in chats:
        tasks = app.task_service.get_all_tasks_on_review(
            chat_id=chat_id, reviewer_id=query.from_user.id
        )
        if not tasks:
            await query.bot.send_message(
                chat_id=query.from_user.id,
                text=f"{task_view.generate_task_header(query.message.chat.title)}"
                f"{Locale.Task.NO_TASKS_MSG}",
            )
            continue

        sent_tasks = 0
        chat = await query.bot.get_chat(chat_id)
        chat_title = "-" if not chat.title else chat.title

        for t in tasks:
            if sent_tasks == app.config.common.task_limit:
                tasks_count = app.task_service.count_tasks_on_review(chat_id=chat_id)
                await query.bot.send_message(
                    text=f"{task_view.generate_task_header(chat_title)}\n"
                    f"{Locale.Error.TO_MANY_UNFINISHED_TASKS}: {tasks_count}\n"
                    f"{Locale.Task.TASK_LIMIT_IS}: {app.config.common.task_limit}",
                    chat_id=query.from_user.id,
                    disable_notification=True,
                )
                break

            await query.bot.send_message(
                text=f"{task_view.generate_task_header(chat_title)}\n"
                f"{task_view.generate_task_body(t)}\n\n"
                f"{common_helpers.generate_link_to_msg(chat_id=t.chat_id, msg_id=t.reply_msg_id)}\n",
                chat_id=query.from_user.id,
                disable_web_page_preview=True,
            )
            sent_tasks += 1


async def send_chat_users_tasks_on_review_to_chat(query: types.CallbackQuery):
    if await is_admin.check(query):
        tasks = app.task_service.get_all_tasks_on_review(chat_id=query.message.chat.id)

        if not tasks:
            await query.bot.send_message(
                chat_id=query.message.chat.id,
                text=f"{task_view.generate_task_header(query.message.chat.title)}"
                f"{Locale.Task.NO_TASKS_MSG}",
            )
            return

        sent_tasks = 0
        task_to_reply_msg_id = []  # (task id | new reply msg | old reply msg )
        for t in tasks:
            if sent_tasks == app.config.common.task_limit:
                tasks_count = app.task_service.count_tasks_on_review(
                    query.message.chat.id
                )
                await query.bot.send_message(
                    text=f"{Locale.Error.TO_MANY_UNFINISHED_TASKS}: {tasks_count}\n"
                    f"{Locale.Task.TASK_LIMIT_IS}: {app.config.common.task_limit}",
                    chat_id=t.chat_id,
                    disable_notification=True,
                )
                break

            msg = await query.bot.send_message(
                text=f"{task_view.generate_task_header(query.message.chat.title)}"
                f"{task_view.generate_task_body(t)}",
                chat_id=t.chat_id,
                reply_markup=keyboards.states_to_keyboards(t.status),
                disable_web_page_preview=True,
            )
            task_to_reply_msg_id.append((t.id, msg.message_id, t.reply_msg_id))

            sent_tasks += 1

        for u in task_to_reply_msg_id:
            app.task_service.set_reply_msg_id(u[0], u[1])
            await query.bot.delete_message(query.message.chat.id, u[2])
    else:
        await error_handlers.show_error_msg_for_n_seconds(
            query=query, error_msg=Locale.Error.ADMIN_RIGHTS_REQUIRED
        )


async def update_view_with_table_data(
    task: TasksModel,
    query: types.CallbackQuery,
    reply_markup: Union[types.InlineKeyboardMarkup, None] = None,
):
    await query.bot.edit_message_text(
        text=task_view.generate_task_body(task),
        chat_id=task.chat_id,
        message_id=task.reply_msg_id,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )
