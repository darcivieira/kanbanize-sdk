from typing import Literal, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseDataClasse:
    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class UsersListParams(BaseDataClasse):
    """
    Query parameters accepted when listing users.
    """
    user_ids: Optional[List] = None
    is_enabled: Optional[Literal[0, 1]] = None
    is_confirmed: Optional[Literal[0, 1]] = None
    if_assigned_where_i_am: Optional[Literal[0, 1]] = None
    fields: Optional[List] = None
    expand: Optional[List] = None


@dataclass
class UsersInsertBody(BaseDataClasse):
    """
    Request body used to create a user.
    """
    email: str


@dataclass
class UsersUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing user.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    is_enabled: Optional[Literal[0, 1]] = None
    is_tfa_enabled: Optional[Literal[0, 1]] = None


@dataclass
class TeamsListParams(BaseDataClasse):
    """
    Query parameters accepted when listing teams.
    """
    team_ids: Optional[List] = None
    name: Optional[str] = None
    fields: Optional[List] = None
    expand: Optional[List] = None


@dataclass
class TeamsInsertBody(BaseDataClasse):
    """
    Request body used to create a team.
    """
    name: str
    description: Optional[str] = None


@dataclass
class TeamsUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing team.
    """
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class WorkspacesListParams(BaseDataClasse):
    """
    Query parameters accepted when listing workspaces.
    """
    workspace_ids: Optional[List] = None
    type: Optional[Literal[1, 2]] = None
    is_archived: Optional[Literal[0, 1]] = None
    if_workspace_manager: Optional[Literal[0, 1]] = None
    if_assigned_to_boards: Optional[Literal[0, 1]] = None
    board_filter_is_archived: Optional[Literal[0, 1]] = None
    board_filter_if_assigned: Optional[Literal[0, 1]] = None


@dataclass
class WorkspacesInsertBody(BaseDataClasse):
    """
    Request body used to create a workspace.
    """
    name: str
    type: Literal[1, 2]


@dataclass
class WorkspacesUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing workspace.
    """
    name: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None

    
@dataclass
class WorkspaceHistoryListParams(BaseDataClasse):
    """
    Query parameters accepted when listing the history of a workspace.
    """
    workspace_ids: Optional[List] = None
    user_ids: Optional[List] = None
    event_types: Optional[List] = None
    _from: Optional[datetime] = None
    to: Optional[datetime] = None
    from_date: Optional[datetime.date] = None
    to_date: Optional[datetime.date] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class BoardsListParams(BaseDataClasse):
    """
    Query parameters accepted when listing boards.
    """
    board_ids: Optional[List] = None
    workspace_ids: Optional[List] = None
    is_archived: Optional[Literal[0, 1]] = None
    if_assigned: Optional[Literal[0, 1]] = None
    fields: Optional[List] = None
    expand: Optional[List] = None


@dataclass
class BoardsInsertBody(BaseDataClasse):
    """
    Request body used to create a board.
    """
    workspace_id: int
    name: str
    description: str


@dataclass
class BoardsUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing board.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None


@dataclass
class BoardSettingsUpdateBody(BaseDataClasse):
    """
    Request body used to update the settings of a board.
    """
    size_type: Optional[int] = None
    allow_exceeding: Optional[int] = None
    autoarchive_cards_after: Optional[int] = None
    limit_type: Optional[int] = None
    allow_repeating_custom_card_ids: Optional[int] = None
    is_discard_reason_required: Optional[int] = None


@dataclass
class BoardHistoryListParams(BaseDataClasse):
    """
    Query parameters accepted when listing the history of a board.

    Parameters:
        board_ids: It's a list of integer number and can be not specified
    """
    board_ids: Optional[List] = None
    user_ids: Optional[List] = None
    event_types: Optional[List] = None
    _from: Optional[datetime] = None
    to: Optional[datetime] = None
    from_date: Optional[datetime.date] = None
    to_date: Optional[datetime.date] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class WorkflowsInsetBody(BaseDataClasse):
    """
    Request body used to create a workflow on a board.
    """
    position: int
    is_enabled: int
    is_collapsible: int
    name: str
    _type: int


@dataclass
class WorkflowsCopyBody(BaseDataClasse):
    """
    Request body used to copy a workflow to a board.
    """
    name: str
    to_board_id: int
    copy_service_level_expectations: int
    copy_column_checklist_items: int


@dataclass
class WorkflowsUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing workflow.
    """
    position: Optional[int] = None
    is_enabled: Optional[int] = None
    is_collapsible: Optional[int] = None
    name: Optional[str] = None
    _type: Optional[int] = None


@dataclass
class LanesListParams(BaseDataClasse):
    """
    Query parameters accepted when listing the lanes of a board.
    """
    fields: Optional[List[str]] = None


@dataclass
class LanesInsertBody(BaseDataClasse):
    """
    Request body used to create a lane on a board.
    """
    workflow_id: int
    parent_lane_id: int
    position: int
    name: str
    color: str
    description: Optional[str] = None


@dataclass
class LanesUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing lane.
    """
    parent_lane_id: Optional[int] = None
    position: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


@dataclass
class ColumnsListParams(LanesListParams):
    """
    Query parameters accepted when listing the columns of a board.
    """
    ...


@dataclass
class ColumnsInsertBody(BaseDataClasse):
    """
    Request body used to create a column on a board.
    """
    workflow_id: int
    section: int
    parent_column_id: int
    position: int
    name: str
    limit: int
    cards_per_row: int
    flow_type: int
    description: Optional[str] = None
    color: Optional[str] = None


@dataclass
class ColumnsUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing column.
    """
    section: Optional[int] = None
    parent_column_id: Optional[int] = None
    position: Optional[int] = None
    name: Optional[str] = None
    limit: Optional[int] = None
    cards_per_row: Optional[int] = None
    flow_type: Optional[int] = None
    description: Optional[str] = None
    color: Optional[str] = None


@dataclass
class CellLimitsUpdateBody(BaseDataClasse):
    """
    Request body used to update the cell limits of a board.
    """
    lane_id: int
    column_id: int
    limit: int


@dataclass
class MergedAreasInsertBody(BaseDataClasse):
    """
    Request body used to create a merged area on a board.
    """
    lane_ids: list
    column_ids: list
    primary_column_id: int
    limit: int


@dataclass
class MergedAreasUpdateBody(BaseDataClasse):
    """
    Request body used to update an existing merged area.
    """
    lane_ids: Optional[List] = None
    column_ids: Optional[List] = None
    primary_column_id: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LaneSectionLimitsUpdateBody(BaseDataClasse):
    """
    Request body used to update the lane section limits of a board.
    """
    lane_id: int
    section: list
    limit: int


@dataclass
class BoardAssigneesUpdateBody(BaseDataClasse):
    """
    Request body used to update an assignee of a board.
    """
    role_id: int


@dataclass
class BoardStickersInsertBody(BaseDataClasse):
    """
    Request body used to add a sticker to a board.
    """
    limit_per_board: int
    limit_per_card: int


@dataclass
class BoardStickersUpdateBody(BaseDataClasse):
    """
    Request body used to update a sticker of a board.
    """
    limit_per_board: Optional[int] = None
    limit_per_card: Optional[int] = None


@dataclass
class BoardCardTypesInsertBody(BaseDataClasse):
    """
    Request body used to add a card type to a board.
    """
    icon_type: int
    icon_id: int
    color: str
    card_color_sync: int


@dataclass
class BoardCardTypesUpdateBody(BaseDataClasse):
    """
    Request body used to update a card type of a board.
    """
    icon_type: Optional[int] = None
    icon_id: Optional[int] = None
    color: Optional[str] = None
    card_color_sync: Optional[int] = None


@dataclass
class BoardCustomFieldsInsertBody(BaseDataClasse):
    """
    Request body used to add a custom field to a board.
    """
    is_always_present: int
    position: int
    display_width: int
    prefix: str
    suffix: str
    unique_values: int
    value_is_required: int
    default_value: str
    inherit_default_value: int
    color: Optional[str] = None


@dataclass
class BoardCustomFieldsUpdateBody(BoardCustomFieldsInsertBody):
    """
    Request body used to update a custom field of a board.
    """
    is_always_present: Optional[int] = None
    position: Optional[int] = None
    display_width: Optional[int] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    unique_values: Optional[int] = None
    value_is_required: Optional[int] = None
    default_value: Optional[str] = None
    inherit_default_value: Optional[int] = None


@dataclass
class BoardCustomFieldAllowedValuesInsertBody(BaseDataClasse):
    """
    Request body used to add an allowed value to a board custom field.
    """
    position: int
    is_default: int


@dataclass
class BoardCustomFieldAllowedValuesUpdateBody(BoardCustomFieldAllowedValuesInsertBody):
    """
    Request body used to update an allowed value of a board custom field.
    """
    position: Optional[int] = None
    is_default: Optional[int] = None


@dataclass
class BoardTeamsUpdateBody(BaseDataClasse):
    """
    Request body used to update a team assigned to a board.
    """
    role_id: int
