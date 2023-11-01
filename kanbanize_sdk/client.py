from .wrapper import KanbanizeSession
from .users import Users
from .teams import Teams
from .managed_workspaces import ManagedWorkspaces
from .workspaces import Workspaces
from .workspace_managers import WorkspaceManagers
from .workspace_history import WorkspaceHistory


class Kanbanize:
    def __init__(self, options):
        self.service = KanbanizeSession(options)

    def users(self):
        return Users(self.service)

    def teams(self):
        return Teams(self.service)

    def managed_workspaces(self):
        return ManagedWorkspaces(self.service)
    
    def workspaces(self):
        return Workspaces(self.service)
    
    def workspace_managers(self):
        return WorkspaceManagers(self.service)
    
    def workspace_history(self):
        return WorkspaceHistory(self.service)