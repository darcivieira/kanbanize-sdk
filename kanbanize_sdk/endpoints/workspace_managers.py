from .workspaces import Workspaces


class WorkspaceManagers(Workspaces):
    """
    Class responsible to make calls to Kanbanize Workspace managers endpoints
    """

    # post= private

    def list(self, workspace_id: int) -> list:
        """
        This method is responsible for listing all workspace managers.

        Parameters:
            workspace_id:  An integer parameter that represents the workspace identification.

        Returns:
            An array of objects that represents the workspace managers
        """
        return self.service.get(self.endpoint + f'/{workspace_id}/managers')
    
    def delete(self, workspace_id: int, user_id: int) -> None:
        """
        This method is responsible to remove a workspace manager.

        Parameters:
            workspace_id: An integer parameter that represents the workspace identification.
            user_id: An integer parameter that represents the manager identification that will be delete.
        
        """
        self.service.delete(self.endpoint + f'/{workspace_id}/managers/{user_id}')

    def get(self, workspace_id: int, user_id: int) -> None:
        """
        This method is responsible to get one workspace manager.

        Parameters:
            workspace_id: An integer parameter that represents the workspace identification.
            user_id: An integer parameter that represents the manager identification.
        """
        self.service.get(self.endpoint + f'/{workspace_id}/managers/{user_id}')

    def update(self, workspace_id: int, user_id: int) -> None:
        """
        This method is responsible to update an workspace manager.

        Parameters:
            workspace_id: An integer parameter that represents the workspace identification.
            user_id: An integer parameter that represents the new manager identification.
        """
        self.service.put(self.endpoint + f'/{workspace_id}/managers/{user_id}')