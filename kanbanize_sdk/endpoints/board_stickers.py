from .generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardStickersInsertBody, BoardStickersUpdateBody


class BoardStickers(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize board stickers endpoints
    """

    endpoint = '/boards'

    def list(self, board_id: int, *args, **kwargs) -> list:
        """
        This method is responsible to list all board stickers from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board assignee

        Returns:
            An array of objects that represents the board stickers

        """
        return self.service.get(self.endpoint + f'/{board_id}/stickers')

    def get(self, board_id: int, sticker_id: int, *args, **kwargs) -> dict:
        """
        This method is responsible to get a board stickers from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            sticker_id: An integer parameter that represents the user identification.

        Returns:
            A board sticker object with the basic information data.
        """
        return self.service.get(self.endpoint + f'/{board_id}/stickers/{sticker_id}')

    def insert(self, board_id: int, sticker_id: int, body: BoardStickersInsertBody, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board stickers from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            sticker_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board stickers to the
                board into the platform.

        Returns:
              An object that represents the board sticker.

        """
        return self.service.put(self.endpoint + f'/{board_id}/stickers/{sticker_id}', data=body.to_dict())

    def update(self, board_id: int, sticker_id: int, body: BoardStickersUpdateBody, *args, **kwargs) -> dict:

        """
        This method is responsible to get a board stickers from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            sticker_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that provide the essential request body needed to update a board stickers to the
                board into the platform.
        """
        return self.service.patch(self.endpoint + f'/{board_id}/stickers/{sticker_id}', data=body.to_dict())

    def delete(self, board_id: int, sticker_id: int, *args, **kwargs) -> None:

        """
        This method is responsible to get a board stickers from the board into the platform.

        Parameters:
            board_id: An integer parameter that represents the board identification.
            sticker_id: An integer parameter that represents the user identification.
        """
        return self.service.delete(self.endpoint + f'/{board_id}/stickers/{sticker_id}')
