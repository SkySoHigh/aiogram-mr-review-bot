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
                          taken_on_review_at: datetime.datetime, reply_msg_id: int) -> TasksModel:
        self.__client.tasks.update_by(values={'reviewer_id': reviewer_id,
                                              'reviewer_name': reviewer_name,
                                              'status': TaskStates.ON_REVIEW,
                                              'taken_on_review_at': taken_on_review_at,
                                              'reply_msg_id': reply_msg_id,
                                              },
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def reject_task_review(self, task_id: int, rejected_from_final_review_at: datetime.datetime) -> TasksModel:
        self.__client.tasks.update_by(values={'status': TaskStates.FIX_REQUIRED,
                                              'rejected_from_final_review_at': rejected_from_final_review_at},
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def resubmit_task_to_review_after_fix(self, task_id: int) -> TasksModel:
        self.__client.tasks.update_by(values={'status': TaskStates.REVIEW_AFTER_FIX},
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def submit_task_to_final_review(self, task_id: int, submitted_to_final_review_at: datetime.datetime) -> TasksModel:
        self.__client.tasks.update_by(values={'submitted_to_final_review_at': submitted_to_final_review_at,
                                              'status': TaskStates.FINAL_REVIEW_REQUIRED,
                                              },
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def accept_final_task_review(self, task_id: int, final_reviewer_name: str,
                                 completed_at: datetime.datetime) -> TasksModel:
        self.__client.tasks.update_by(values={'final_reviewer_name': final_reviewer_name,
                                              'completed_at': completed_at,
                                              'status': TaskStates.VERIFIED,
                                              },
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def reject_final_task_review(self, task_id: int, rejected_from_final_review_at: datetime.datetime) -> TasksModel:
        self.__client.tasks.update_by(values={'submitted_to_final_review_at': None,
                                              'rejected_from_final_review_at': rejected_from_final_review_at,
                                              'status': TaskStates.FIX_REQUIRED,
                                              },
                                      id=task_id)
        return self.get_task_by_id(task_id=task_id)

    def get_task_by_id(self, task_id) -> TasksModel:
        return self.__client.tasks.read_by(id=task_id)[0]

    def get_all_new_tasks(self, chat_id: int) -> List[TasksModel]:
        return self.__client.tasks.read_by(status=TaskStates.NEW, chat_id=chat_id)

    def get_all_tasks_on_review(self, chat_id: int, reviewer_id: int = None) -> List[TasksModel]:
        statuses = [TaskStates.NEW, TaskStates.ON_REVIEW, TaskStates.FIX_REQUIRED, TaskStates.FINAL_REVIEW_REQUIRED]
        if reviewer_id:
            return self.__client.tasks.read_by_status_with_filter(status=statuses,
                                                                  reviewer_id=reviewer_id,
                                                                  chat_id=chat_id,
                                                                  )
        else:
            return self.__client.tasks.read_by_status_with_filter(status=statuses,
                                                                  chat_id=chat_id,
                                                                  )

    def count_tasks_on_review(self, chat_id: int, reviewer_id: int = None) -> int:
        statuses = [TaskStates.NEW, TaskStates.ON_REVIEW, TaskStates.FIX_REQUIRED, TaskStates.FINAL_REVIEW_REQUIRED]
        if reviewer_id:
            return self.__client.tasks.get_count_by_status_with_filter(
                status=statuses,
                reviewer_id=reviewer_id,
                chat_id=chat_id)
        else:
            return self.__client.tasks.get_count_by_status_with_filter(status=statuses,
                                                                       chat_id=chat_id,
                                                                       )

    def set_reply_msg_id(self, task_id: int, reply_msg_id: int):
        return self.__client.tasks.update_by(values={'reply_msg_id': reply_msg_id},
                                             id=task_id,
                                             )

    def get_all_reviewer_chats_ids(self, reviewer_id: int) -> List[int]:
        return [item for sublist in
                self.__client.tasks.get_distinct_chats_ids_from_tasks_with_filter(reviewer_id=reviewer_id) for item in
                sublist]
