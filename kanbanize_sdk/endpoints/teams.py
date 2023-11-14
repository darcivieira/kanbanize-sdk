from kanbanize_sdk.endpoints.generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import TeamsListParams, TeamsInsertBody, TeamsUpdateBody


class Teams(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize teams endpoints
    """
    endpoint = '/teams'

    def list(self, params: TeamsListParams | dict | None = None) -> list:
        """
        This method is responsible to list all teams in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the teams.

        Returns:
            An array of objects that represents the teams
        """

        params = params.to_dict() if isinstance(params, TeamsListParams) else params

        return self.service.get(self.endpoint, params=params)

    def insert(self, body: TeamsInsertBody | dict) -> dict:
        """
        This method is responsible to invite a team to the platform.

        Parameters:
            body: It's a dataclass object that provide the essential request body needed to invite a team to the platform.

        Returns:
            A team object with the basic information data
        """

        payload = body.to_dict() if isinstance(body, TeamsInsertBody) else body

        return self.service.post(self.endpoint, data=payload)

    def get(self, team_id: int) -> dict:
        """
        This method is responsible to get one team from the platform.

        Parameters:
            team_id: An integer parameter that represents the team identification.

        Returns:
            A searched team object
        """
        return self.service.get(self.endpoint + f'/{team_id}')

    def update(self, team_id: int, body: TeamsUpdateBody | dict) -> dict:
        """
        This method is responsible to update a team in the platform.

        Parameters:
            team_id: An integer parameter that represents the team identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated team object
        """

        payload = body.to_dict() if isinstance(body, TeamsUpdateBody) else body

        return self.service.patch(self.endpoint + f'/{team_id}', data=payload)

    def delete(self, team_id: int) -> None:
        """
        This method is responsible to remove a Team from the platform.

        Parameters:
            team_id: An integer parameter that represents the team identification.

        Returns:
            None

        """
        self.service.delete(self.endpoint + f'/{team_id}')
