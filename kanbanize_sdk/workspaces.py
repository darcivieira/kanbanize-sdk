from .generics import GenericRequestMethod
from .dataclasses import WorkspacesListParams, WorkspacesInsertBody, WorkspacesUpdateBody


class Workspaces(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize Workspaces endpoints
    """
    endpoint = '/workspaces'

    def list(self, params: WorkspacesListParams | None = None) -> list:
        """
        This method is responsible to list all workspaces in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the workspaces.

        Returns:
            An array of objects that represents the workspaces
        """
        return self.service.get(self.endpoint, params=params)
    
    def insert(self, body: WorkspacesInsertBody) -> dict:
        """
        This method is responsible to add a workspace to the platform.

        Parameters:
            body: It's a dataclass object that provide the essential request body needed to add an workspace to the platform.

        Returns:
            An workspace object with the basic information data
        """
        return self.service.post(self.endpoint, data=body.to_dict())

    def get(self, workspace_id: int) -> dict:
        """
        This method is responsible to get one workspace from the platform.

        Parameters:
            workspace_id: An integer parameter that represents the workspace identification.

        Returns:
            A searched workspace object
        """
        return self.service.get(self.endpoint + f'/{workspace_id}')

    def update(self, workspace_id: int, body: WorkspacesUpdateBody) -> dict:
        """
        This method is responsible to update an workspace in the platform.

        Parameters:
            workspace_id: An integer parameter that represents the workspace identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated workspace object
        """
        return self.service.patch(self.endpoint + f'/{workspace_id}', data=body.to_dict())