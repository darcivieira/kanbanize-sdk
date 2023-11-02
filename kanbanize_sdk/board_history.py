from .boards import Boards
from .dataclasses import BoardHistoryListParams
from .utils import private


class BoardHistory(Boards):
    """
    Class responsible to make calls to Kanbanize board structure endpoints
    """

    get = private

    insert = private

    update = private

    delete = private

    def list(self, params: BoardHistoryListParams | None = None) -> list:
        """
        This method is responsible to list all board in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the boards.

        Returns:
            An array of objects that represents the boards
        """
        params = params.to_dict() if params else None
        return self.service.get(self.endpoint + '/history', params=params)
