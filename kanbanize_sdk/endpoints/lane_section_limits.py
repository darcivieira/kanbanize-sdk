from kanbanize_sdk.utils import private
from kanbanize_sdk.dataclasses import LaneSectionLimitsUpdateBody

from .generics import GenericRequestMethod


class LaneSectionLimits(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize lane section limits endpoints
    """
    endpoint = '/boards'

    get = private

    delete = private

    insert = private

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all lane section limits from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the selected board object.

        Returns:
            An array with multiples lane section limit objects

        """
        return self.service.get(self.endpoint + f'/{board_id}/laneSectionLimits')

    def update(self, board_id: int, body: LaneSectionLimitsUpdateBody, *args, **kwargs) -> dict:
        """
        This method is responsible to update one lane section limit from the board into the platform.

        Parameters:
            board_id: An integer that represents the selected board object.
            body: It's a dataclass object that provide all needed request body to update a cell limit object.

        Returns:
             An lane section limit object with the basic information data.

        """
        return self.service.put(self.endpoint + f'/{board_id}/laneSectionLimits', data=body.to_dict())
