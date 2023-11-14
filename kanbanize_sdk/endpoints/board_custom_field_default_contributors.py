from .generics import GenericRequestMethod


class BoardCustomFieldDefaultContributors(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board custom field default contributors endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, field_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board custom field default contributors from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee
            field_id: An integer parameter that represents the field identification.

        Returns:
            An array of objects that represents the board custom field default contributors

        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields/{field_id}/defaultContributors')

    def get(self, board_id: int, field_id: int, user_id: int, *args, **kwargs) -> None:
        """
        This method is responsible to get a board custom field default contributors from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            user_id: An integer parameter that represents the user identification.

        Returns:
            A board custom field default contributor object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/customFields/{field_id}/defaultContributors/{user_id}')

    def update(self,
               board_id: int,
               field_id: int,
               user_id: int,
               *args,
               **kwargs) -> None:

        """
        This method is responsible to get a board custom field default contributors from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            user_id: An integer parameter that represents the user identification.
        """
        return self.service.put(self.endpoint + f'/{board_id}/customFields/{field_id}/defaultContributors/{user_id}')

    def delete(self, board_id: int, field_id: int, user_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board custom field default contributors from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            field_id: An integer parameter that represents the field identification.
            user_id: An integer parameter that represents the user identification.

        """
        return self.service.delete(self.endpoint + f'/{board_id}/customFields/{field_id}/defaultContributors/{user_id}')


