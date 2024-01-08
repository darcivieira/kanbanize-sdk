from kanbanize_sdk.endpoints.generics import GenericRequestMethod


class DashboardPagesUsers(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize users dashboard pages endpoints
    """
    endpoint = '/dashboardPages'

    def list(self, dashboard_page_id: int) -> list:
        """
        This method is responsible to get a list of the users having access to a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.

        Returns:
            A list of the users having access to a dashboard page.
        """

        return self.service.get(
            self.endpoint + f'/{dashboard_page_id}/users',
        )

    def get(self, dashboard_page_id: int, user_id: int) -> dict:
        """
        This method is responsible to get one user from the platform.

        Parameters:
            dashboard_page_id: A dashboard page id.
            user_id: A user id.

        Returns:
            The user is added to the dashboard page! Otherwise, you would have gotten a 404 error.
        """
        return self.service.get(self.endpoint + f'/{dashboard_page_id}/users/{user_id}')

    def update(self, dashboard_page_id: int, user_id: int) -> dict:
        """
        This method is responsible to give a user access to a dashboard page or set/unset as a manager of a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.
            user_id: A user id.

        Returns:
            The user is added to the dashboard page or is set/unset as a manager of the dashboard page! Otherwise, you would have gotten a 404 error.
        """

        return self.service.put(self.endpoint + f'/{dashboard_page_id}/users/{user_id}')

    def delete(self, dashboard_page_id: int, user_id: int) -> None:
        """
        This method is responsible to deny a user access to a dashboard page.

        Parameters:
            dashboard_page_id: A dashboard page id.
            user_id: A user id.

        """
        self.service.delete(self.endpoint + f'/{dashboard_page_id}/users/{user_id}')
