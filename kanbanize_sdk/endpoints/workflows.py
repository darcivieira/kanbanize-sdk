from kanbanize_sdk.endpoints.generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import WorkflowsInsetBody, WorkflowsUpdateBody, WorkflowsCopyBody


class Workflows(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize workflows endpoints
    """
    endpoint = '/boards'

    def list(self, board_id: int) -> list:
        """
        This method is responsible to list all workflows from a board in the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.

        Returns:
            An array of objects that represents the workflows
        """
        return self.service.get(self.endpoint + f'/{board_id}/workflows')

    def insert(self, board_id: int, body: WorkflowsInsetBody) -> dict:
        """
        This method is responsible to insert a workflow to the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            body: It's a dataclass object that provide the essential request body needed to add a board to the platform.

        Returns:
            A workflow object with the basic information data
        """
        return self.service.post(self.endpoint + f'/{board_id}/workflows', data=body.to_dict())

    def get(self, board_id: int, workflow_id: int) -> dict:
        """
        This method is responsible to get one workflow from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            workflow_id: An integer parameter that represents the workflow identification.

        Returns:
            A searched workflow object
        """
        return self.service.get(self.endpoint + f'/{board_id}/workflows/{workflow_id}')

    def update(self, board_id: int, workflow_id: int, body: WorkflowsUpdateBody) -> dict:
        """
        This method is responsible to update one workflow from a board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            workflow_id: An integer parameter that represents the workflow identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated workflow object
        """
        return self.service.patch(self.endpoint + f'/{board_id}/workflows/{workflow_id}', data=body.to_dict())

    def delete(self, board_id: int, workflow_id: int) -> None:
        """
        This method is responsible to remove a workflow from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            workflow_id: An integer parameter that represents the workflow identification.

        """
        return self.service.delete(self.endpoint + f'/{board_id}/workflows/{workflow_id}')

    def copy(self, board_id: int, workflow_id: int, body: WorkflowsCopyBody) -> dict:
        """
        This method is responsible to make a copy of one workflow from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            workflow_id: An integer parameter that represents the workflow identification.
            body: It's a dataclass object that represent the body option to be coped.

        Returns:
            A workflow object with the basic information data
        """
        return self.service.post(self.endpoint + f'/{board_id}/workflows/{workflow_id}/copy', data=body.to_dict())
