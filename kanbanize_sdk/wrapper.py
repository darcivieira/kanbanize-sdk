import json
from typing import Any, TypedDict

import httpx


class DefaultOptions(TypedDict):
    subdomain: str
    api_key: str


class KanbanizeSession:
    """
    Transport layer for the Kanbanize API v2.

    This class composes an httpx client instead of inheriting from it, so the
    public surface of the SDK stays limited to what it actually promises. See
    specs/arquitetura/adr/ for the decision record.
    """

    def __init__(self, options: DefaultOptions, **kwargs):
        self.__uri = f'https://{options.get("subdomain")}.kanbanize.com/api/v2'
        self.__api_key = options.get("api_key")
        self.__client = httpx.Client(
            headers={'Content-Type': 'application/json', 'apikey': self.__api_key},
            **kwargs
        )

    @property
    def uri(self):
        return self.__uri

    @property
    def api_key(self):
        return self.__api_key

    def request(self, method, url=None, data=None, headers=None, **kwargs) -> httpx.Response:
        return self.__client.request(method, self.uri + url, data=data, **kwargs)

    def get(self, url, **kwargs) -> Any:
        r = self.request('GET', url, **kwargs)
        return self.__middleware_response(r)

    def post(self, url, data=None, json=None, **kwargs) -> dict:
        r = self.request('POST', url, data=data, json=json, **kwargs)
        return self.__middleware_response(r)

    def put(self, url, data=None, json=None, **kwargs) -> Any:
        r = self.request('PUT', url, data=data, json=json, **kwargs)
        return self.__middleware_response(r)

    def patch(self, url, data=None, json=None, **kwargs) -> dict:
        r = self.request('PATCH', url, data=data, json=json, **kwargs)
        return self.__middleware_response(r)

    def delete(self, url, **kwargs) -> None:
        r = self.request('DELETE', url, **kwargs)
        return self.__middleware_response(r)

    @staticmethod
    def __middleware_response(r: httpx.Response) -> dict | None | list:
        status_message = {
            500: {'code': 500, 'message': 'The request failed due to an internal server error.'},
            503: {'code': 503, 'message': 'The service is temporarily unavailable.'},
            0: 'There was an unexpected error when making the request.'
        }

        if r.status_code in [200, 204]:
            response = json.loads(r.content) if r.status_code == 200 else None
            if response:
                if response.get('pagination'):
                    new_response = response.pop('pagination')
                    new_response.update(response)
                    return new_response
                return response.get('data')
            return None

        response = json.loads(r.content) \
            if r.status_code in [400, 401, 403, 404, 409, 429] else status_message.get(r.status_code)

        # Behaviour preserved as-is from the requests-based implementation: for 500 and 503 the
        # dict above has no 'error' key, so this raises ValueError(None) and the message is never
        # delivered. Changing it would change what callers observe. Tracked in visao/ROADMAP.md.
        raise ValueError(
            response.get('error') if response else {'code': r.status_code, 'message': status_message.get(0)}
        )
