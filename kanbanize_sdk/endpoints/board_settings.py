from .boards import Boards
from kanbanize_sdk.dataclasses import BoardSettingsUpdateBody
from kanbanize_sdk.utils import private


class BoardSettings(Boards):
    """
    Class responsible to make calls to Kanbanize board settings endpoints
    """

    list = private

    insert = private

    delete = private

    def get(self, board_id: int) -> dict:
        """
        This method is responsible to get one board settings from the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            A searched board object
        """
        return self.service.get(self.endpoint + f'/{board_id}/settings')

    def update(self, board_id: int, body: BoardSettingsUpdateBody) -> dict:
        """
        This method is responsible to update one board settings in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated board object
        """
        return self.service.patch(self.endpoint + f'/{board_id}/settings', data=body.to_dict())
