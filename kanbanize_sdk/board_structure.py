from .boards import Boards
from .utils import private


class BoardStructure(Boards):
    """
    Class responsible to make calls to Kanbanize board structure endpoints
    """

    list = private

    insert = private

    update = private

    delete = private

    def get(self, board_id: int) -> dict:
        """
        This method is responsible to get one board structure from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/currentStructure')

    def get_revision(self, board_id: int) -> dict:
        """
        This method is responsible to get one board structure revision from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/currentStructure/revision')
