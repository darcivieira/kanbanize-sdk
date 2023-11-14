from .generics import GenericRequestMethod


class BoardTags(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board tags endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board tags from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board tags

        """
        return self.service.get(self.endpoint + f'/{board_id}/tags')

    def get(self, board_id: int, tag_id: int, *args, **kwargs) -> None:
        """
        This method is responsible to get a board tag from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            tag_id: An integer parameter that represents the reason identification.

        Returns:
            A board tag object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/tags/{tag_id}')

    def update(self, board_id: int, tag_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board tag from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            tag_id: An integer parameter that represents the reason identification.
        """
        return self.service.put(self.endpoint + f'/{board_id}/tags/{tag_id}')

    def delete(self, board_id: int, tag_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board tag from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            tag_id: An integer parameter that represents the reason identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/tags/{tag_id}')




