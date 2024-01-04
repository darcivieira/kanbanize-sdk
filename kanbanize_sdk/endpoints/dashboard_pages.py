from kanbanize_sdk.endpoints.generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import DashboardPagesListParams, DashboardPagesInsetBody, DashboardPagesUpdateBody


class DashboardPages(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize dashboard pages endpoints
    """
    endpoint = '/dashboardPages'

    def list(self, params: DashboardPagesListParams | dict | None = None) -> list:
        """
        This method is responsible to list all dashboard pages in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the dashboard pages.

        Returns:
            An array of objects that represents the dashboard pages
        """

        params = params.to_dict() if isinstance(params, DashboardPagesListParams) else params

        return self.service.get(
            self.endpoint,
            params=params
        )

    def insert(self, body: DashboardPagesInsetBody | dict) -> dict:
        """
        This method is responsible to invite a dashboard page to the platform.

        Parameters:
            body: It's a dataclass object that provide the essential request body needed to create a dashboard page to
            the platform.

        Returns:
            A dashboard page object with the basic information data
        """

        payload = body.to_dict() if isinstance(body, DashboardPagesInsetBody) else body

        return self.service.post(self.endpoint, data=payload)

    def get(self, dashboard_page_id: int) -> dict:
        """
        This method is responsible to get one dashboard page from the platform.

        Parameters:
            dashboard_page_id: An integer parameter that represents the dashboard page identification.

        Returns:
            A searched dashboard page object
        """
        return self.service.get(self.endpoint + f'/{dashboard_page_id}')

    def update(self, dashboard_page_id: int, body: DashboardPagesUpdateBody | dict) -> dict:
        """
        This method is responsible to update a dashboard page in the platform.

        Parameters:
            dashboard_page_id: An integer parameter that represents the dashboard page identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated dashboard page object
        """

        payload = body.to_dict() if isinstance(body, DashboardPagesUpdateBody) else body

        return self.service.patch(self.endpoint + f'/{dashboard_page_id}', data=payload)

    def delete(self, dashboard_page_id: int) -> None:
        """
        This method is responsible to remove a dashboard page from the platform.

        Parameters:
            dashboard_page_id: An integer parameter that represents the dashboard page identification.

        """
        self.service.delete(self.endpoint + f'/{dashboard_page_id}')
