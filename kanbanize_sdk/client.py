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
    MergedAreas,
    LaneSectionLimits,
    BoardAssignees,
    BoardTeams,
    BoardTags,
    BoardVisibleStandardFields,
    BoardStickers,
    BoardCustomFields,
    BoardDiscardReasons,
    BoardCardTypes,
    BoardCustomFieldAllowedValues,
    BoardCustomFieldDefaultContributors,
    BoardChildParentCards,
    BoardCardTemplates,
    BoardBlockReasons,
)
from .wrapper import KanbanizeSession


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

    def merged_areas(self):
        return MergedAreas(self.service)

    def lane_section_limits(self):
        return LaneSectionLimits(self.service)

    def board_assignees(self):
        return BoardAssignees(self.service)

    def board_teams(self):
        return BoardTeams(self.service)

    def board_tags(self):
        return BoardTags(self.service)

    def board_visible_standard_fields(self):
        return BoardVisibleStandardFields(self.service)

    def board_stickers(self):
        return BoardStickers(self.service)

    def board_custom_fields(self):
        return BoardCustomFields(self.service)

    def board_custom_field_default_contributors(self):
        return BoardCustomFieldDefaultContributors(self.service)

    def board_custom_field_allowed_values(self):
        return BoardCustomFieldAllowedValues(self.service)

    def board_discard_reasons(self):
        return BoardDiscardReasons(self.service)

    def board_card_types(self):
        return BoardCardTypes(self.service)

    def board_card_templates(self):
        return BoardCardTemplates(self.service)

    def board_child_parent_cards(self):
        return BoardChildParentCards(self.service)

    def board_block_reasons(self):
        return BoardBlockReasons(self.service)
