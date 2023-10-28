from .wrapper import KanbanizeSession
from .users import Users
from .teams import Teams
from .managed_workspaces import ManagedWorkspaces


class Kanbanize:
    def __init__(self, options):
        self.service = KanbanizeSession(options)

    def users(self):
        return Users(self.service)

    def teams(self):
        return Teams(self.service)

    def managedWorkspace(self):
        return ManagedWorkspaces(self.service)