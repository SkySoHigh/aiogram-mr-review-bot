from db.controllers.tasks import TasksController
from db.transport import DbTransport

__all__ = ["DBClient"]


class DBClient:
    def __init__(self, transport: DbTransport):
        """Database client, which provides access for all db controllers and methods.

        Args:
            transport (DbTransport): Class providing transport to communicate with db
        """
        self.__transport = transport
        self.tasks = TasksController(self.__transport)

    @property
    def transport(self) -> DbTransport:
        return self.__transport
