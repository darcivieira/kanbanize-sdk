from kanbanize_sdk.dataclasses import LanesListParams, LanesInsertBody, LanesUpdateBody

from .generics import GenericRequestMethod


class Lanes(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize lanes endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, params: LanesListParams | None = None, *args, **kwargs) -> list:
        """
        This method is responsible to list all lanes from a board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            params: It's a dataclass object that provide all possible parameters to be used to list the lanes.

        Returns:
            An array of objects that represents the lanes
        """
        return self.service.get(self.endpoint + f'/{board_id}/lanes', params=params)

    def insert(self, board_id: int, body: LanesInsertBody, *args, **kwargs) -> dict:
        """
        This method is responsible to insert a lane to the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that provide the essential request body needed to add a lane to the board into
                the platform.

        Returns:
            A lane object with the basic information data
        """
        return self.service.post(self.endpoint + f'/{board_id}/lanes', data=body.to_dict())

    def get(self, board_id: int, lane_id: int, *args, **kwargs):
        """
        This method is responsible to get a lane from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            lane_id: An integer parameter that represents the lane identification.

        Returns:
            A lane object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/lanes/{lane_id}')

    def update(self, board_id: int, lane_id: int, body: LanesUpdateBody,  *args, **kwargs) -> dict:
        """
        This method is responsible to update a lane from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board selected.
            lane_id: An integer parameter that represents the lane selected.
            body: It's a dataclass object that provide all lane essential fields to be updated.
        Returns:
            A lane object with the basic information data
        """
        return self.service.patch(self.endpoint + f'/{board_id}/lanes/{lane_id}', data=body.to_dict())

    def delete(self, board_id: int, lane_id: int, *args, **kwargs) -> None:
        """
        This method is responsible to update a lane from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board selected.
            lane_id: An integer parameter that represents the lane selected.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/lanes/{lane_id}')
