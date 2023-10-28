from .generics import GenericRequestMethod


class ManagedWorkspaces(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize managed korkpaces endpoints
    """
    endpoint = '/users'

    def list(self, user_id: int) -> list:
        """
        This method is responsible to get one managed workpaces from the platform.

        Parameters:
            user_id: An integer parameter that represents the user identification.

        Returns:
            A list searched workspace_id object
        """
        return self.service.get(self.endpoint + f'/{user_id}/managedWorkspaces')