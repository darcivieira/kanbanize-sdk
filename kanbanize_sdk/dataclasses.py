from typing import Literal, List, Optional
from dataclasses import dataclass


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
