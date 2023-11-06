from .wrapper import KanbanizeSession
from .endpoints import (
    Users,
    Teams,
    ManagedWorkspaces,
    Workspaces,
    WorkspaceManagers,
    WorkspaceHistory,
    Boards,
    BoardSettings,
    BoardStructure,
    BoardStructureRevisions,
    BoardHistory,
    Workflows,
    Lanes,
    Columns,
    CellLimits,
)


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

    def workflows(self):
        return Workflows(self.service)

    def lanes(self):
        return Lanes(self.service)

    def columns(self):
        return Columns(self.service)

    def cell_limits(self):
        return CellLimits(self.service)
