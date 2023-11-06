from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import ColumnsListParams, ColumnsInsertBody, ColumnsUpdateBody


class Columns(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize columns endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, params: ColumnsListParams | None = None, *args, **kwargs):
        """
        This method is responsible to list all columns from board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            params: It's a dataclass object that provide all possible parameters to be used to list the columns.

        Returns:
            An array of objects that represents the columns

        """
        return self.service.get(
            self.endpoint + f'/{board_id}/columns',
            params=params.to_dict() if isinstance(params, ColumnsListParams) else params
        )

    def insert(self, board_id: int, body: ColumnsInsertBody, *args, **kwargs):
        """
        This method is responsible to add a column to the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            body: It's a dataclass object that provide the essential request body needed to add a column
                to the platform.

        Returns:
            A column object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/columns', data=body.to_dict())

    def get(self, board_id: int, column_id: int, *args, **kwargs):
        """
        This method is responsible to get one column object from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            column_id: An integer parameter that represents the selected column object.

        Returns:
            A column object with the basic information data.

        """
        return self.service.get(self.endpoint + f'/{board_id}/columns/{column_id}')

    def patch(self, board_id: int, column_id: int, body: ColumnsUpdateBody, *args, **kwargs):
        """
        This method is responsible to update one column object from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            column_id: An integer parameter that represents the selected column object.
            body: It's a dataclass object that provide the essential request body needed to update a column
                to the platform.

        Returns:
            A column object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/columns/{column_id}', data=body.to_dict())

    def delete(self, board_id: int, column_id: int, *args, **kwargs):
        """
        This method is responsible to delete one column object from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            column_id: An integer parameter that represents the selected column object.
        """
        return self.service.get(self.endpoint + f'/{board_id}/columns/{column_id}')
