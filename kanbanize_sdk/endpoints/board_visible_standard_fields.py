from .generics import GenericRequestMethod


class BoardVisibleStandardFields(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board visible standard fields endpoints
    """

    endpoint = '/boards'
    ...

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board visible standard fields from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board visible standard fields

        """
        return self.service.get(self.endpoint + f'/{board_id}/visibleStandardFields')

    def get(self, board_id: int, field_name: int, *args, **kwargs) -> None:
        """
        This method is responsible to get a board visible standard field from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_name: An integer parameter that represents the field name identification.

        Returns:
            A board visible standard field object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/visibleStandardFields/{field_name}')

    def update(self, board_id: int, field_name: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board visible standard field from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_name: An integer parameter that represents the field name identification.
        """
        return self.service.put(self.endpoint + f'/{board_id}/visibleStandardFields/{field_name}')

    def delete(self, board_id: int, field_name: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board visible standard field from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_name: An integer parameter that represents the field name identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/visibleStandardFields/{field_name}')


