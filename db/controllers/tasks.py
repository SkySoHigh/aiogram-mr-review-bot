from db.controllers.base import BaseDBController
from db.models.tasks import TasksModel


class TasksController(BaseDBController[TasksModel]):
    ...
