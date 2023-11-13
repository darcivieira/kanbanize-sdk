from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardCustomFieldAllowedValuesInsertBody, BoardCustomFieldAllowedValuesUpdateBody


class BoardCustomFieldAllowedValues(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board custom field allowed values endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, field_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board custom field allowed values from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee
            field_id: An integer parameter that represents the field identification.

        Returns:
            An array of objects that represents the board custom field allowed values

        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields/{field_id}/allowedValues')

    def get(self, board_id: int, field_id: int, value_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board custom field allowed values from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            value_id: An integer parameter that represents the value identification.

        Returns:
            A board custom field allowed value object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields/{field_id}/allowedValues/{value_id}')

    def insert(self,
               board_id: int,
               field_id: int,
               value_id: int,
               body: BoardCustomFieldAllowedValuesInsertBody,
               *args,
               **kwargs) -> dict:

        """
        This method is responsible to get a board custom field allowed values from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            value_id: An integer parameter that represents the value identification.
            body: It's a dataclass object that provide the essential request body needed to update a board custom field allowed values to the
                board into the platform.

        Returns:
              An object that represents the board custom field allowed value.

        """
        return self.service.put(
            self.endpoint + f'/{board_id}/customFields/{field_id}/allowedValues/{value_id}', data=body.to_dict()
        )

    def update(self,
               board_id: int,
               field_id: int,
               value_id: int,
               body: BoardCustomFieldAllowedValuesUpdateBody,
               *args,
               **kwargs) -> dict:

        """
        This method is responsible to get a board custom field allowed values from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            value_id: An integer parameter that represents the value identification.
            body: It's a dataclass object that provide the essential request body needed to update a board custom field allowed values to the
                board into the platform.
        """
        return self.service.patch(
            self.endpoint + f'/{board_id}/customFields/{field_id}/allowedValues/{value_id}', data=body.to_dict()
        )

    def delete(self, board_id: int, field_id: int, value_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board custom field allowed values from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            value_id: An integer parameter that represents the value identification.

        """
        return self.service.delete(self.endpoint + f'/{board_id}/customFields/{field_id}/allowedValues/{value_id}')


