from kanbanize_sdk.users import Users
from .utils import private



class ManagedWorkspaces(Users):
    """
    Class responsible to make calls to Kanbanize managed workpaces endpoints
    """

    insert = private

    get = private

    update = private

    delete = private

    def list(self, user_id: int) -> list:
        """
        This method is responsible to get one managed workpaces from the platform.

        Parameters:
            user_id: An integer parameter that represents the user identification.

        Returns:
            A list searched workspace_id object
        """
        return self.service.get(self.endpoint + f'/{user_id}/managedWorkspaces')