import re
from typing import Union

from aiogram import types

from db.models.tasks import TasksModel
from locales import Locale
from utils import pprint_datetime


def generate_task_body(task_model: TasksModel) -> str:
    return f'{Locale.Task.ID}: {task_model.id}\n' \
           f'{Locale.Task.STATUS}: {task_model.status.name}\n' \
           f'{Locale.Task.URL}: {task_model.url}\n' \
           f'\n' \
           f'{Locale.Task.PUBLISHED_BY}: @{task_model.publisher_name}\n' \
           f'{Locale.Task.PUBLISHED_AT}: {pprint_datetime(task_model.published_at)}\n' \
           f'\n' \
           f'{Locale.Task.REVIEWED_BY}: @{task_model.reviewer_name}\n' \
           f'{Locale.Task.TAKEN_TO_REVIEW_AT}: {pprint_datetime(task_model.taken_on_review_at)}\n' \
           f'\n' \
           f'{Locale.Task.SUBMITTED_TO_FINAL_REVIEW}: {pprint_datetime(task_model.submitted_to_final_review_at)}\n' \
           f'\n' \
           f'{Locale.Task.COMPLETED_AT}: {pprint_datetime(task_model.completed_at)}\n' \
           f'{Locale.Task.COMPLETED_BY}: @{task_model.final_reviewer_name}'


def get_id_from_view_text(message: str) -> int:
    try:
        return re.findall(pattern=Locale.Task.ID + ":\s(\\d+)", string=message)[0]
    except KeyError:
        raise KeyError  # !TODO raise normal exception


def generate_task_header(query: Union[types.Message, types.CallbackQuery]) -> str:
    return f'{Locale.Common.CHAT_ORIGIN_MSG} {query.message.chat.title}\n\n'
