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
    Set here a documentation
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
    Set here a documentation
    """
    email: str


@dataclass
class UsersUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    email: Optional[str] = None
    username: Optional[str] = None
    is_enabled: Optional[Literal[0, 1]] = None
    is_tfa_enabled: Optional[Literal[0, 1]] = None


@dataclass
class TeamsListParams(BaseDataClasse):
    """
    Set here a documentation
    """
    team_ids: Optional[List] = None
    name: Optional[str] = None
    fields: Optional[List] = None
    expand: Optional[List] = None


@dataclass
class TeamsInsertBody(BaseDataClasse):
    """
    Set here a documentation
    """
    name: str
    description: Optional[str] = None


@dataclass
class TeamsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class WorkspacesListParams(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation
    """
    name: str
    type: Literal[1, 2]


@dataclass
class WorkspacesUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    name: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None

    
@dataclass
class WorkspaceHistoryListParams(BaseDataClasse):
    """
    Set here a documentation
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

    
class BoardsListParams(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation
    """
    workspace_id: int
    name: str
    description: str


@dataclass
class BoardsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    name: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None


@dataclass
class BoardSettingsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation

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
    Set here a documentation
    """
    position: int
    is_enabled: int
    is_collapsible: int
    name: str
    _type: int


@dataclass
class WorkflowsCopyBody(BaseDataClasse):
    """
    Set here a documentation
    """
    name: str
    to_board_id: int
    copy_service_level_expectations: int
    copy_column_checklist_items: int


@dataclass
class WorkflowsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    position: Optional[int] = None
    is_enabled: Optional[int] = None
    is_collapsible: Optional[int] = None
    name: Optional[str] = None
    _type: Optional[int] = None


@dataclass
class LanesListParams(BaseDataClasse):
    """
    Set here a documentation
    """
    fields: Optional[List[str]] = None


@dataclass
class LanesInsertBody(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation
    """
    parent_lane_id: Optional[int] = None
    position: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


@dataclass
class ColumnsListParams(LanesListParams):
    """
    Set here a documentation
    """
    ...


@dataclass
class ColumnsInsertBody(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation
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
    Set here a documentation
    """
    lane_id: int
    column_id: int
    limit: int


@dataclass
class MergedAreasInsertBody(BaseDataClasse):
    """
    Set here a documentation
    """
    lane_ids: list
    column_ids: list
    primary_column_id: int
    limit: int


@dataclass
class MergedAreasUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    lane_ids: Optional[List] = None
    column_ids: Optional[List] = None
    primary_column_id: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LaneSectionLimitsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    lane_id: int
    section: list
    limit: int


@dataclass
class BoardAssigneesUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    role_id: int


@dataclass
class BoardStickersInsertBody(BaseDataClasse):
    """
    Set here a documentation
    """
    limit_per_board: int
    limit_per_card: int


@dataclass
class BoardStickersUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    limit_per_board: Optional[int] = None
    limit_per_card: Optional[int] = None


@dataclass
class BoardCardTypesInsertBody(BaseDataClasse):
    """
    Set here a documentation
    """
    icon_type: int
    icon_id: int
    color: str
    card_color_sync: int


@dataclass
class BoardCardTypesUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    icon_type: Optional[int] = None
    icon_id: Optional[int] = None
    color: Optional[str] = None
    card_color_sync: Optional[int] = None


@dataclass
class BoardCustomFieldsInsertBody(BaseDataClasse):
    """
    Set here a documentation
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
    Set here a documentation
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
    Set here a documentation
    """
    position: int
    is_default: int


@dataclass
class BoardCustomFieldAllowedValuesUpdateBody(BoardCustomFieldAllowedValuesInsertBody):
    """
    Set here a documentation
    """
    position: Optional[int] = None
    is_default: Optional[int] = None


@dataclass
class BoardTeamsUpdateBody(BaseDataClasse):
    """
    Set here a documentation
    """
    role_id: int


@dataclass
class DashboardPagesListParams(BaseDataClasse):
    """
    Ste here a documentation
    """
    dashboard_page_ids: Optional[List[int]] = None
    fields: Optional[List[str]] = None


@dataclass
class DashboardPagesInsetBody(BaseDataClasse):
    """
    Ste here a documentation
    """
    name: str


@dataclass
class DashboardPagesUpdateBody(BaseDataClasse):
    """
    Ste here a documentation
    """
    name: str
