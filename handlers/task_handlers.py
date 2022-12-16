import asyncio
import re
from datetime import datetime

from aiogram import types

from common import app
from db.models.tasks import TasksModel, TaskStates
from keyboard.keyboards import get_tasks_on_review_menu, get_tasks_submitted_menu
from locales import Locale


async def periodic_reminder(sleep_for=5):
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.utcnow()
        await app.bot.send_message(340541141, f"{now}")


async def publish_task_for_review(message: types.Message):
    if len(message.text.split(' ', 1)) != 2:
        await message.reply(Locale.Error.INCORRECT_REVIEW_SUBMIT_COMMAND, disable_notification=True)
    else:
        task = TasksModel(url=message.text.strip().split(' ', 1)[1],
                          status=TaskStates.NEW,
                          origin_chat=message.chat.id,
                          msg_id=message.message_id,
                          applicant=message.from_user.id,
                          application_time=message.date)
        app.db_client.tasks.create(task)
        await message.reply(text=f'{Locale.NewTaskOnReview.NEW_TASK_MSG}\n'
                                 f'-> {task.id}',
                            reply_markup=get_tasks_on_review_menu(),
                            disable_notification=True
                            )


async def set_global_reminder(message: types.Message):
    if not app.periodic_task:
        await message.reply("There is no background task. Creating")
        app.periodic_task = asyncio.ensure_future(periodic_reminder())


async def unset_global_reminder(message: types.Message):
    if not app.periodic_task:
        await message.reply("There is no background task. Creating")
        app.periodic_task = asyncio.ensure_future(periodic_reminder())


async def take_review_task(query: types.CallbackQuery):
    await query.answer()

    # TODO: Gets integer from text by splitting text on '->' and extracting int
    task_id = re.findall('[0-9]+', query.message.text.split('->', 1)[1])[0]
    app.db_client.tasks.update_by(id=task_id,
                                  values={'status': TaskStates.ON_REVIEW,
                                          'acceptance_time': datetime.now(),
                                          'reviewer': query.from_user.id,
                                          'msg_id': query.message.message_id
                                          })
    task = app.db_client.tasks.read_by(id=task_id)[0]

    reviewer = await app.bot.get_chat_member(task.origin_chat, task.reviewer)

    await app.bot.edit_message_text(text=f'{Locale.TaskSubmitted.SUBMITTED_MSG_ACCEPTED_TIME} {task.acceptance_time}\n'
                                         f'{Locale.TaskSubmitted.SUBMITTED_MSG_ACCEPTED_BY} {reviewer.user.first_name} {reviewer.user.last_name}\n'
                                         f'-> {task.id}',
                                    chat_id=task.origin_chat,
                                    message_id=task.msg_id,
                                    reply_markup=get_tasks_submitted_menu())


async def confirm_review_task(query: types.CallbackQuery):
    await query.answer()
    # TODO: Gets integer from text by splitting text on '->' and extracting int
    task_id = re.findall('[0-9]+', query.message.text.split('->', 1)[1])[0]

    task = app.db_client.tasks.read_by(id=task_id)[0]

    db_reviewer = await app.bot.get_chat_member(task.origin_chat, task.reviewer)
    current_reviewer = await app.bot.get_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)

    if current_reviewer.user.id in [db_reviewer.user.id, *app.config.common.admins]:
        acceptance_time = datetime.now()
        app.db_client.tasks.update_by(id=task_id,
                                      values={'status': TaskStates.COMPLETED,
                                              'acceptance_time': acceptance_time})
        text = [
            f'{Locale.TaskConfirmed.CONFIRMED_MSG_COMPLETION_TIME} {acceptance_time}',
            f'{Locale.TaskSubmitted.SUBMITTED_MSG_ACCEPTED_BY} {db_reviewer.user.first_name} {db_reviewer.user.last_name}',
            f'-> {task.id}'
        ]

        await app.bot.edit_message_text(text='\n'.join(text), chat_id=task.origin_chat, message_id=task.msg_id)

        # If msg edited from pm = update both
        if task.msg_id != query.message.message_id:
            await app.bot.edit_message_text(text='\n'.join(text), chat_id=query.message.chat.id,
                                            message_id=query.message.message_id)

    else:
        await query.message.reply(text=Locale.Error.UNABLE_TO_CONFIRM_TASK_BY_ANY_USER)
