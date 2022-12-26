from typing import List, Union

from sqlalchemy import func

from db.controllers import BaseDBController
from db.models import TasksModel, TaskStates


class TasksController(BaseDBController[TasksModel]):
    def read_by_status_with_filter(
        self,
        *,
        limit: int = 1000,
        status: Union[TaskStates, List[TaskStates]],
        **filter_kwargs
    ) -> List[TasksModel]:
        with self.transport() as session:
            if isinstance(status, list):
                return (
                    session.query(self.model)
                    .filter(self.model.status.in_(status))
                    .filter_by(**filter_kwargs)
                    .limit(limit)
                    .all()
                )
            else:
                return (
                    session.query(self.model)
                    .filter(self.model.status == status)
                    .filter_by(**filter_kwargs)
                    .limit(limit)
                    .all()
                )

    def get_count_by_status_with_filter(
        self, *, status: Union[TaskStates, List[TaskStates]], **filter_kwargs
    ) -> int:
        with self.transport() as session:
            if isinstance(status, list):
                return (
                    session.query(func.count(self.model.id))
                    .filter(self.model.status.in_(status))
                    .filter_by(**filter_kwargs)
                    .scalar()
                )
            else:
                return (
                    session.query(func.count(self.model.id))
                    .filter(self.model.status == status)
                    .filter_by(**filter_kwargs)
                    .scalar()
                )

    def get_distinct_chats_ids_from_tasks_with_filter(
        self, **filter_kwargs
    ) -> List[tuple]:
        with self.transport() as session:
            return (
                session.query(self.model.chat_id)
                .filter_by(**filter_kwargs)
                .distinct()
                .all()
            )
