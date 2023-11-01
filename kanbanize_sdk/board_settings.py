from .boards import Boards
from .dataclasses import BoardsUpdateBody
from .utils import private


class BoardSettings(Boards):
    """
    Class responsible to make calls to Kanbanize boards endpoints
    """

    list = private

    insert = private

    delete = private

    def get(self, board_id: int) -> dict:
        """
        This method is responsible to get one board from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/settings')

    def update(self, board_id: int, body: BoardsUpdateBody) -> dict:
        """
        This method is responsible to update an board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated board object
        """
        return self.service.patch(self.endpoint + f'/{board_id}/settings', data=body.to_dict())
