from .generics import GenericRequestMethod


class BoardCardTemplates(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board card templates endpoints
    """

    endpoint = '/boards'
    ...

    # def list(self, board_id: int, *args, **kwargs) -> list:
    #     """
    #     This method is responsible to list all board discard reasons from the board into the platform.
    #
    #     Parameters:
    #         board_id: An integer parameter that represents the board assignee
    #
    #     Returns:
    #         An array of objects that represents the board discard reasons
    #
    #     """
    #     return self.service.get(self.endpoint + f'/{board_id}/discardReasons')
    #
    # def get(self, board_id: int, reason_id: int, *args, **kwargs) -> None:
    #     """
    #     This method is responsible to get a board discard reason from the board into the platform.
    #
    #     Parameters:
    #         board_id: An integer parameter that represents the board identification.
    #         reason_id: An integer parameter that represents the reason identification.
    #
    #     Returns:
    #         A board discard reason object with the basic information data.
    #     """
    #     return self.service.get(self.endpoint + f'/{board_id}/discardReasons/{reason_id}')
    #
    # def update(self, board_id: int, reason_id: int, *args, **kwargs) -> None:
    #
    #     """
    #     This method is responsible to get a board discard reason from the board into the platform.
    #
    #     Parameters:
    #         board_id: An integer parameter that represents the board identification.
    #         reason_id: An integer parameter that represents the reason identification.
    #     """
    #     return self.service.put(self.endpoint + f'/{board_id}/discardReasons/{reason_id}')
    #
    # def delete(self, board_id: int, reason_id: int, *args, **kwargs) -> None:
    #
    #     """
    #     This method is responsible to get a board discard reason from the board into the platform.
    #
    #     Parameters:
    #         board_id: An integer parameter that represents the board identification.
    #         reason_id: An integer parameter that represents the reason identification.
    #     """
    #     return self.service.delete(self.endpoint + f'/{board_id}/discardReasons/{reason_id}')


