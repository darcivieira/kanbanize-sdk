from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import MergedAreasInsertBody, MergedAreasUpdateBody


class MergedAreas(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize merged areas endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all merged areas from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the merged area

        Returns:
            An array of objects that represents the merged areas

        """
        return self.service.get(self.endpoint + f'/{board_id}/mergedAreas')

    def insert(self, board_id: int, body: MergedAreasInsertBody, *args, **kwargs) -> dict:
        """
        This method is responsible to insert a merged areas to the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that provide the essential request body needed to add a merged areas to the
                board into the platform.

        Returns:
            A merged area object with the basic information data
        """
        return self.service.post(self.endpoint + f'/{board_id}/mergedAreas', data=body.to_dict())

    def get(self, board_id: int, area_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a merged areas from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            area_id: An integer parameter that represents the merged area identification.

        Returns:
            A merged area object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/mergedAreas/{area_id}')

    def update(self, board_id: int, area_id: int, body: MergedAreasUpdateBody, *args, **kwargs) -> dict:

        """
        This method is responsible to get a merged areas from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            area_id: An integer parameter that represents the merged area identification.
            body: It's a dataclass object that provide the essential request body needed to update a merged areas to the
                board into the platform.

        Returns:
            A merged area object with the basic information data.
        """
        return self.service.patch(self.endpoint + f'/{board_id}/mergedAreas/{area_id}', data=body.to_dict())

    def delete(self, board_id: int, area_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a merged areas from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            area_id: An integer parameter that represents the merged area identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/mergedAreas/{area_id}')
