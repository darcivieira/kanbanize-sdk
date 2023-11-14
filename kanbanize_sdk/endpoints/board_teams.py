from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardTeamsUpdateBody


class BoardTeams(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board teams endpoints
    """

    endpoint = '/boards'
    ...

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board teams from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board teams

        """
        return self.service.get(self.endpoint + f'/{board_id}/teams')

    def get(self, board_id: int, team_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to get a board team from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            team_id: An integer parameter that represents the team identification.

        Returns:
            A board team object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/teams/{team_id}')

    def update(self, board_id: int, team_id: int, body: BoardTeamsUpdateBody | dict,  *args, **kwargs) -> None:

        """
        This method is responsible to get a board team from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            team_id: An integer parameter that represents the team identification.
            body: It's a dataclass object that provide the essential request body needed to update a board team fields
                to the board into the platform.
        """

        payload = body.to_dict() if isinstance(body, BoardTeamsUpdateBody) else body

        return self.service.put(self.endpoint + f'/{board_id}/teams/{team_id}', data=payload)

    def delete(self, board_id: int, team_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board team from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            team_id: An integer parameter that represents the team identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/teams/{team_id}')
