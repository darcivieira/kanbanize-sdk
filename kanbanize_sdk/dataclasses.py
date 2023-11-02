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
        return {
            key.strip('_'): list(map(str, value)) if isinstance(value, list) else value
            for key, value in self.__dict__.items() if value is not None
        }

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
