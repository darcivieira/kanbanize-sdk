from kanbanize_sdk.endpoints.generics import GenericRequestMethod


class DashboardPagesTeams(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize users endpoints
    """
    endpoint = '/dashboardPages'

    def list(self, dashboard_page_id: int) -> list:
        """
        This method is responsible to get a list of the teams having access to a dashboard page.

        Parameters:
            dashboard_page_id: An integer parameter that represents the dashboard page identification.

        Returns:
            A list of the teams having access to a dashboard page
        """

        return self.service.get(
            self.endpoint + f'/{dashboard_page_id}/teams'
        )

    def get(self, dashboard_page_id: int, team_id: int) -> None:
        """
        This method is responsible to check if a team is added to a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.
            team_id: A team id.

        Returns:
            The team is added to the dashboard page! Otherwise, you would have gotten a 404 error
        """
        self.service.get(self.endpoint + f'/{dashboard_page_id}/teams/{team_id}')

    def update(self, dashboard_page_id: int, team_id: int) -> None:
        """
        This method is responsible to give a team access to a dashboard page or set/unset as a manager of a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.
            team_id: A team id.

        Returns:
            The team is added to the dashboard page or is set/unset as a manager of the dashboard page! Otherwise, you would have gotten a 404 error.
        """

        self.service.put(self.endpoint + f'/{dashboard_page_id}/teams/{team_id}')

    def delete(self, dashboard_page_id: int, team_id: int) -> None:
        """
        This method is responsible to deny a team access to a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.
            team_id: A team id.
        """

        self.service.delete(self.endpoint + f'/{dashboard_page_id}/teams/{team_id}')
