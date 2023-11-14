from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardCardTypesInsertBody, BoardCardTypesUpdateBody


class BoardCardTypes(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board card types endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board card types from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board card types

        """
        return self.service.get(self.endpoint + f'/{board_id}/cardTypes')

    def get(self, board_id: int, type_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board card types from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            type_id: An integer parameter that represents the user identification.

        Returns:
            A board card type object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/cardTypes/{type_id}')

    def get_effective_settings(self, board_id: int, type_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board card type settings from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            type_id: An integer parameter that represents the user identification.

        Returns:
            A board card type settings object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/cardTypes/{type_id}/effectiveSettings')

    def insert(self, board_id: int, type_id: int, body: BoardCardTypesInsertBody | dict, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board card types from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            type_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board card types to the
                board into the platform.

        Returns:
              An object that represents the board card type.

        """

        payload = body.to_dict() if isinstance(body, BoardCardTypesInsertBody) else body

        return self.service.put(self.endpoint + f'/{board_id}/cardTypes/{type_id}', data=payload)

    def update(self, board_id: int, type_id: int, body: BoardCardTypesUpdateBody | dict, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board card types from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            type_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board card types to the
                board into the platform.
        """

        payload = body.to_dict() if isinstance(body, BoardCardTypesUpdateBody) else body

        return self.service.patch(self.endpoint + f'/{board_id}/cardTypes/{type_id}', data=payload)

    def delete(self, board_id: int, type_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board card types from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            type_id: An integer parameter that represents the user identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/cardTypes/{type_id}')

