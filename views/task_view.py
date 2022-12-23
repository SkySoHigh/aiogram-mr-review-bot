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
           f'{Locale.Task.REJECTED_AT}: {pprint_datetime(task_model.rejected_from_final_review_at)}\n' \
           f'\n' \
           f'{Locale.Task.COMPLETED_AT}: {pprint_datetime(task_model.completed_at)}\n' \
           f'{Locale.Task.COMPLETED_BY}: @{task_model.final_reviewer_name}'


def generate_task_header(chat_title: str) -> str:
    return f'{Locale.Common.CHAT_ORIGIN_MSG} {chat_title}\n\n'
