from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import ColumnsListParams, ColumnsInsertBody, ColumnsUpdateBody


class Columns(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize columns endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, params: ColumnsListParams | dict | None = None, *args, **kwargs) -> list:
        """
        This method is responsible to list all columns from board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            params: It's a dataclass object that provide all possible parameters to be used to list the columns.

        Returns:
            An array of objects that represents the columns
        """

        params = params.to_dict() if isinstance(params, ColumnsListParams) else params

        return self.service.get(
            self.endpoint + f'/{board_id}/columns',
            params=params
        )

    def insert(self, board_id: int, body: ColumnsInsertBody | dict, *args, **kwargs) -> dict:
        """
        This method is responsible to add a column to the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            body: It's a dataclass object that provide the essential request body needed to add a column
                to the platform.

        Returns:
            A column object with the basic information data.
        """

        payload = body.to_dict() if isinstance(body, ColumnsInsertBody) else body

        return self.service.post(self.endpoint + f'/{board_id}/columns', data=payload)

    def get(self, board_id: int, column_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get one column object from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            column_id: An integer parameter that represents the selected column object.

        Returns:
            A column object with the basic information data.

        """
        return self.service.get(self.endpoint + f'/{board_id}/columns/{column_id}')

    def update(self, board_id: int, column_id: int, body: ColumnsUpdateBody | dict, *args, **kwargs) -> dict:
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

        payload = body.to_dict() if isinstance(body, ColumnsUpdateBody) else body

        return self.service.patch(self.endpoint + f'/{board_id}/columns/{column_id}', data=payload)

    def delete(self, board_id: int, column_id: int, *args, **kwargs) -> None:
        """
        This method is responsible to delete one column object from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.
            column_id: An integer parameter that represents the selected column object.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/columns/{column_id}')
