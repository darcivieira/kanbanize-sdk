from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardAssigneesUpdateBody


class BoardAssignees(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board assignees endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board assignees from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board assignees

        """
        return self.service.get(self.endpoint + f'/{board_id}/userRoles')

    def get(self, board_id: int, user_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board assignees from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            user_id: An integer parameter that represents the user identification.

        Returns:
            A board assignee object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/userRoles/{user_id}')

    def update(self, board_id: int, user_id: int, body: BoardAssigneesUpdateBody | dict, *args, **kwargs) -> None:

        """
        This method is responsible to get a board assignees from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            user_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board assignees to the
                board into the platform.
        """

        payload = body.to_dict() if isinstance(body, BoardAssigneesUpdateBody) else body

        return self.service.put(
            self.endpoint + f'/{board_id}/userRoles/{user_id}',
            data=payload
        )

    def delete(self, board_id: int, user_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board assignees from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            user_id: An integer parameter that represents the user identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/userRoles/{user_id}')
