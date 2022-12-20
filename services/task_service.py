import datetime
from typing import List

from db.client import DBClient
from db.models.tasks import TasksModel, TaskStates


class TaskService:
    def __init__(self, client: DBClient):
        self.__client = client

    def create_task(self, url: str, chat_id: int, publisher_msg_id: int, publisher_id: int, publisher_name: str,
                    published_at: str) -> int:
        task = TasksModel(url=url,
                          status=TaskStates.NEW,
                          chat_id=chat_id,
                          publisher_msg_id=publisher_msg_id,
                          publisher_id=publisher_id,
                          publisher_name=publisher_name,
                          published_at=published_at,
                          )

        self.__client.tasks.create(task)
        return task.id

    def set_task_reviewer(self, task_id: int, reviewer_id: int, reviewer_name: str,
                          taken_on_review_at: datetime.datetime, reply_msg_id: int) -> None:
        return self.__client.tasks.update_by(values={'reviewer_id': reviewer_id,
                                                     'reviewer_name': reviewer_name,
                                                     'status': TaskStates.ON_REVIEW,
                                                     'taken_on_review_at': taken_on_review_at,
                                                     'reply_msg_id': reply_msg_id,
                                                     },
                                             id=task_id)

    def submit_task_to_final_review(self, task_id: int, submitted_to_final_review_at: datetime.datetime):
        return self.__client.tasks.update_by(values={'submitted_to_final_review_at': submitted_to_final_review_at,
                                                     'status': TaskStates.FINAL_REVIEW_REQUIRED,
                                                     },
                                             id=task_id)

    def complete_task_review(self, task_id: int, final_reviewer_name: str, completed_at: datetime.datetime):
        return self.__client.tasks.update_by(values={'final_reviewer_name': final_reviewer_name,
                                                     'completed_at': completed_at,
                                                     'status': TaskStates.COMPLETED,
                                                     },
                                             id=task_id)

    def reject_task_review(self, task_id: int):
        return self.__client.tasks.update_by(values={'submitted_to_final_review_at': None,
                                                     'status': TaskStates.ON_REVIEW,
                                                     },
                                             id=task_id)

    def get_task_by_id(self, task_id) -> TasksModel:
        return self.__client.tasks.read_by(id=task_id)[0]

    def get_all_new_tasks(self, chat_id: int) -> List[TasksModel]:
        return self.__client.tasks.read_by(status=TaskStates.NEW, chat_id=chat_id)

    def get_all_tasks_on_review(self, chat_id: int, reviewer_id: int = None) -> List[TasksModel]:
        if reviewer_id:
            return self.__client.tasks.read_by_status_with_filter(
                status=[TaskStates.ON_REVIEW, TaskStates.FINAL_REVIEW_REQUIRED], reviewer_id=reviewer_id,
                chat_id=chat_id)
        else:
            return self.__client.tasks.read_by_status_with_filter(status=[TaskStates.ON_REVIEW,
                                                                          TaskStates.FINAL_REVIEW_REQUIRED],
                                                                  chat_id=chat_id)

    def count_tasks_on_review(self, chat_id: int, reviewer_id: int = None) -> int:
        if reviewer_id:
            return self.__client.tasks.get_count_by_status_with_filter(
                status=[TaskStates.ON_REVIEW, TaskStates.FINAL_REVIEW_REQUIRED], reviewer_id=reviewer_id,
                chat_id=chat_id)
        else:
            return self.__client.tasks.get_count_by_status_with_filter(status=[TaskStates.ON_REVIEW,
                                                                               TaskStates.FINAL_REVIEW_REQUIRED],
                                                                       chat_id=chat_id)

    def set_reply_msg_id(self, task_id: int, reply_msg_id: int):
        return self.__client.tasks.update_by(values={'reply_msg_id': reply_msg_id},
                                             id=task_id,
                                             )
