from .generics import GenericRequestMethod
from .dataclasses import UsersListParams, UsersInsertBody, UsersUpdateBody


class Users(GenericRequestMethod):

    __endpoint = '/users'

    def list(self, params: UsersListParams | None = None):
        params = params.to_dict() if params else None
        return self.service.get(self.endpoint, params=params)

    def insert(self, body: UsersInsertBody):
        return self.service.post(self.endpoint, data=body.to_dict())

    def get(self, user_id: int):
        return self.service.get(self.endpoint + f'/{user_id}')

    def update(self, user_id: int, body: UsersUpdateBody):
        return self.service.patch(self.endpoint + f'/{user_id}', data=body.to_dict())

    def delete(self, user_id):
        return self.service.delete(self.endpoint + f'/{user_id}')
