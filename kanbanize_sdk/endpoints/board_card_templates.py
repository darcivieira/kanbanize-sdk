from .generics import GenericRequestMethod


class BoardCardTemplates(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board card templates endpoints
    """

    endpoint = '/boards'
    ...

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board card templates from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board card templates

        """
        return self.service.get(self.endpoint + f'/{board_id}/cardTemplates')

    def get(self, board_id: int, template_id: int, *args, **kwargs) -> None:
        """
        This method is responsible to get a board card template from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            template_id: An integer parameter that represents the template identification.

        Returns:
            A board card template object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/cardTemplates/{template_id}')

    def update(self, board_id: int, template_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board card template from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            template_id: An integer parameter that represents the template identification.
        """
        return self.service.put(self.endpoint + f'/{board_id}/cardTemplates/{template_id}')

    def delete(self, board_id: int, template_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board card template from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            template_id: An integer parameter that represents the template identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/cardTemplates/{template_id}')


