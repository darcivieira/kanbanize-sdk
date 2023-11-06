from typing import Literal, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UsersListParams:
    user_ids: Optional[List] = None
    is_enabled: Optional[Literal[0, 1]] = None
    is_confirmed: Optional[Literal[0, 1]] = None
    if_assigned_where_i_am: Optional[Literal[0, 1]] = None
    fields: Optional[List] = None
    expand: Optional[List] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class UsersInsertBody:
    email: str

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class UsersUpdateBody:
    email: Optional[str] = None
    username: Optional[str] = None
    is_enabled: Optional[Literal[0, 1]] = None
    is_tfa_enabled: Optional[Literal[0, 1]] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class TeamsListParams:
    team_ids: Optional[List] = None
    name: Optional[str] = None
    fields: Optional[List] = None
    expand: Optional[List] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class TeamsInsertBody:
    name: str
    description: Optional[str] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class TeamsUpdateBody:
    name: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class WorkspacesListParams:
    workspace_ids: Optional[List] = None
    type: Optional[Literal[1, 2]] = None
    is_archived: Optional[Literal[0, 1]] = None
    if_workspace_manager: Optional[Literal[0, 1]] = None
    if_assigned_to_boards: Optional[Literal[0, 1]] = None
    board_filter_is_archived: Optional[Literal[0, 1]] = None
    board_filter_if_assigned: Optional[Literal[0, 1]] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class WorkspacesInsertBody:
    name: str
    type: Literal[1, 2]

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class WorkspacesUpdateBody:
    name: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

    
@dataclass
class WorkspaceHistoryListParams:
    workspace_ids: Optional[List] = None
    user_ids: Optional[List] = None
    event_types: Optional[List] = None
    _from: Optional[datetime] = None
    to: Optional[datetime] = None
    from_date: Optional[datetime.date] = None
    to_date: Optional[datetime.date] = None
    page: Optional[int] = None
    per_page: Optional[int] = None

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }

    
class BoardsListParams:
    board_ids: Optional[List] = None
    workspace_ids: Optional[List] = None
    is_archived: Optional[Literal[0, 1]] = None
    if_assigned: Optional[Literal[0, 1]] = None
    fields: Optional[List] = None
    expand: Optional[List] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class BoardsInsertBody:
    workspace_id: int
    name: str
    description: str

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class BoardsUpdateBody:
    name: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[Literal[0, 1]] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class BoardSettingsUpdateBody:
    size_type: Optional[int] = None
    allow_exceeding: Optional[int] = None
    autoarchive_cards_after: Optional[int] = None
    limit_type: Optional[int] = None
    allow_repeating_custom_card_ids: Optional[int] = None
    is_discard_reason_required: Optional[int] = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class BoardHistoryListParams:
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

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class WorkflowsInsetBody:
    """
    Set here a documentation
    """
    position: int
    is_enabled: int
    is_collapsible: int
    name: str
    _type: int

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class WorkflowsCopyBody:
    """
    Set here a documentation
    """
    name: str
    to_board_id: int
    copy_service_level_expectations: int
    copy_column_checklist_items: int

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class WorkflowsUpdateBody:
    """
    Set here a documentation
    """
    position: Optional[int] = None
    is_enabled: Optional[int] = None
    is_collapsible: Optional[int] = None
    name: Optional[str] = None
    _type: Optional[int] = None

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class LanesListParams:
    fields: Optional[List[str]]

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class LanesInsertBody:
    workflow_id: int
    parent_lane_id: int
    position: int
    name: str
    description: Optional[str]
    color: str

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }


@dataclass
class LanesUpdateBody:
    parent_lane_id: Optional[int] = None
    position: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self):
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }
