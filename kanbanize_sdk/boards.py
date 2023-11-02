from .generics import GenericRequestMethod
from .dataclasses import BoardsListParams, BoardsInsertBody, BoardsUpdateBody


class Boards(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize boards endpoints
    """
    endpoint = '/boards'

    def list(self, params: BoardsListParams | None = None) -> list:
        """
        This method is responsible to list all board in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the boards.

        Returns:
            An array of objects that represents the boards
        """
        params = params.to_dict() if params else None
        return self.service.get(self.endpoint, params=params)

    def insert(self, body: BoardsInsertBody) -> dict:
        """
        This method is responsible to invite a board to the platform.

        Parameters:
            body: It's a dataclass object that provide the essential request body needed to invite an board to the platform.

        Returns:
            An board object with the basic information data
        """
        return self.service.post(self.endpoint, data=body.to_dict())

    def get(self, board_id: int) -> dict:
        """
        This method is responsible to get one board from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}')

    def update(self, board_id: int, body: BoardsUpdateBody) -> dict:
        """
        This method is responsible to update an board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated board object
        """
        return self.service.patch(self.endpoint + f'/{board_id}', data=body.to_dict())

    def delete(self, board_id: int) -> None:
        """
        This method is responsible to remove an board from the platform.

        Parameters:
            board_id: Teste

        """
        return self.service.delete(self.endpoint + f'/{board_id}')
