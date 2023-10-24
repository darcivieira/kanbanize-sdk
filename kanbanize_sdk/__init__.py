from .wrapper import KanbanizeSession
from .users import Users
from .dataclasses import (
    UsersListParams,
    UsersInsertBody,
    UsersUpdateBody,
)


class Kanbanize:
    def __init__(self, options):
        self.service = KanbanizeSession(options)

    def users(self):
        return Users(self.service)
