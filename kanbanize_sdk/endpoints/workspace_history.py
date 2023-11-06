from kanbanize_sdk.endpoints.workspaces import Workspaces
from kanbanize_sdk.dataclasses import WorkspaceHistoryListParams


class WorkspaceHistory(Workspaces):
    """
    Class responsible to make calls to Kanbanize Workspace histories endpoints
    """

    # post= private
    # insert = private
    # get = private
    # update = private

    def list(self, params: WorkspaceHistoryListParams | None = None) -> list:
        """
        This method is responsible for listing all workspace histories.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the workspace histories.

        Returns:
            An array of objects representing the workspace histories
        """
        return self.service.get(self.endpoint + '/history', params=params)
