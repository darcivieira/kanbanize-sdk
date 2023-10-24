from .wrapper import KanbanizeSession
from .users import Users

class Kanbanize:
    def __init__(self, options):
        self.service = KanbanizeSession(options)

    def users(self):
        return Users(self.service)