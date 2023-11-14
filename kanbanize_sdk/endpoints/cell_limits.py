from kanbanize_sdk.utils import private
from kanbanize_sdk.dataclasses import CellLimitsUpdateBody

from .generics import GenericRequestMethod


class CellLimits(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize cell limits endpoints
    """
    endpoint = '/boards'

    get = private

    delete = private

    insert = private

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all cell limits from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.

        Returns:
            An array with multiples cell limit objects

        """
        return self.service.get(self.endpoint + f'/{board_id}/cellLimits')

    def update(self, board_id: int, body: CellLimitsUpdateBody | dict, *args, **kwargs) -> dict:
        """
        This method is responsible to update one cell limit from the board into the platform.

        Parameters:
            board_id: An integer that represents the selected board object.
            body: It's a dataclass object that provide all needed request body to update a cell limit object.

        Returns:
             An cell limit object with the basic information data.

        """

        payload = body.to_dict() if isinstance(body, CellLimitsUpdateBody) else body

        return self.service.put(self.endpoint + f'/{board_id}/cellLimits', data=payload)
