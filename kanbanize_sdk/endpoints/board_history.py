from .boards import Boards
from kanbanize_sdk.dataclasses import BoardHistoryListParams
from kanbanize_sdk.utils import private


class BoardHistory(Boards):
    """
    Class responsible to make calls to Kanbanize board history endpoints
    """

    get = private

    insert = private

    update = private

    delete = private

    def list(self, params: BoardHistoryListParams | dict | None = None, *args, **kwargs) -> list:
        """
        This method is responsible to list all board history in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the board history.

        Returns:
            An array of objects that represents the boards
        """

        params = params.to_dict() if isinstance(params, BoardHistoryListParams) else params

        return self.service.get(self.endpoint + '/history', params=params)
