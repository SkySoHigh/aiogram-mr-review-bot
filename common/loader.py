from asyncio import Task

from aiogram import Dispatcher, Bot

from configs import ConfigProvider
from db.client import DBClient
from db.models.base import Base
from db.transport import DbTransport
from services import TaskService


class Loader:
    def __init__(self):
        # Config and common parts
        self.config = ConfigProvider()
        self.bot = Bot(token=self.config.common.token.get_secret_value())
        self.dp = Dispatcher(bot=self.bot)
        self.__periodic_task = None

        # Db client and services
        self.__db_client = DBClient(transport=DbTransport(
            url=self.config.db.dsn,
            echo=self.config.db.echo_db_queries,
            echo_pool=self.config.db.echo_db_pool
        ))

        self.task_service = TaskService(client=self.__db_client)

    @property
    def periodic_task(self) -> Task:
        return self.__periodic_task

    @periodic_task.setter
    def periodic_task(self, coroutine: Task):
        self.__periodic_task = coroutine

    def init_db(self):
        Base.metadata.create_all(self.__db_client.transport.engine)
