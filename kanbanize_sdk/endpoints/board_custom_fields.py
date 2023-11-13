from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardCustomFieldsInsertBody, BoardCustomFieldsUpdateBody


class BoardCustomFields(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board custom fields endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board custom fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board custom fields

        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields')

    def get(self, board_id: int, field_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board custom fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the user identification.

        Returns:
            A board custom field object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields/{field_id}')

    def insert(self, board_id: int, field_id: int, body: BoardCustomFieldsInsertBody, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board custom fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board custom fields to the
                board into the platform.

        Returns:
              An object that represents the board custom field.

        """
        return self.service.put(self.endpoint + f'/{board_id}/customFields/{field_id}', data=body.to_dict())

    def update(self, board_id: int, field_id: int, body: BoardCustomFieldsUpdateBody, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board custom fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board custom fields to the
                board into the platform.
        """
        return self.service.patch(self.endpoint + f'/{board_id}/customFields/{field_id}', data=body.to_dict())

    def delete(self, board_id: int, field_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board custom fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the user identification.

        """
        return self.service.delete(self.endpoint + f'/{board_id}/customFields/{field_id}')
