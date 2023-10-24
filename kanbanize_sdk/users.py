from .generics import GenericRequestMethod
from .dataclasses import UsersListParams, UsersInsertBody, UsersUpdateBody


class Users(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize users endpoints
    """
    endpoint = '/users'

    def list(self, params: UsersListParams | None = None) -> list:
        """
        This method is responsible to list all user in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the users.

        Returns:
            An array of objects that represents the users
        """
        params = params.to_dict() if params else None
        return self.service.get(self.endpoint, params=params)

    def insert(self, body: UsersInsertBody) -> dict:
        """
        This method is responsible to invite a user to the platform.

        Parameters:
            body: It's a dataclass object that provide the essential request body needed to invite an user to the platform.

        Returns:
            An user object with the basic information data
        """
        return self.service.post(self.endpoint, data=body.to_dict())

    def get(self, user_id: int) -> dict:
        """
        This method is responsible to get one user from the platform.

        Parameters:
            user_id: An integer parameter that represents the user identification.

        Returns:
            A searched user object
        """
        return self.service.get(self.endpoint + f'/{user_id}')

    def update(self, user_id: int, body: UsersUpdateBody) -> dict:
        """
        This method is responsible to update an user in the platform.

        Parameters:
            user_id: An integer parameter that represents the user identification.
            body: It's a dataclass object that represent the body option to be updated.

        Returns:
            The updated user object
        """
        return self.service.patch(self.endpoint + f'/{user_id}', data=body.to_dict())

    def delete(self, user_id: int) -> None:
        """
        This method is responsible to remove an user from the platform.

        Parameters:
            user_id: Teste

        """
        return self.service.delete(self.endpoint + f'/{user_id}')
