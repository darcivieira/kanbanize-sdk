from .wrapper import KanbanizeSession
from .users import Users
from .teams import Teams
from .managed_workspaces import ManagedWorkspaces
from .workspaces import Workspaces
from .workspace_managers import WorkspaceManagers
from .workspace_history import WorkspaceHistory
from .boards import Boards
from .board_settings import BoardSettings
from .board_structure import BoardStructure
from .board_structure_revisions import BoardStructureRevisions
from .board_history import BoardHistory


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
    
    def boards(self):
        return Boards(self.service)

    def board_settings(self):
        return BoardSettings(self.service)

    def board_structure(self):
        return BoardStructure(self.service)

    def board_structure_revisions(self):
        return BoardStructureRevisions(self.service)

    def board_history(self):
        return BoardHistory(self.service)
