from .boards import Boards
from kanbanize_sdk.utils import private


class BoardStructureRevisions(Boards):
    """
    Class responsible to make calls to Kanbanize board structure revisions endpoints
    """

    list = private

    insert = private

    update = private

    delete = private

    def get(self, board_id: int) -> dict:
        """
        This method is responsible to get one board from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/structureRevisions')

    def get_revision(self, board_id: int, revision: int) -> dict:
        """
        This method is responsible to get one board from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            revision: An integer parameter that represents the revision identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/structureRevisions/{revision}')
