import json
from typing import Any, TypedDict
from dataclasses import dataclass

from requests import Session, Response, RequestException
from requests.structures import CaseInsensitiveDict


class DefaultOptions(TypedDict):
    subdomain: str
    api_key: str


class KanbanizeSession(Session):
    def __init__(self, options: DefaultOptions, **kwargs):
        self.__uri = f'https://{options.get("subdomain")}.kanbanize.com/api/v2'
        self.__api_key = options.get("api_key")
        super(KanbanizeSession, self).__init__(**kwargs)

    @property
    def uri(self):
        return self.__uri

    @property
    def api_key(self):
        return self.__api_key

    def request(self, method, url=None, data=None, headers=None, **kwargs) -> Response:
        headers = {'Content-Type': 'application/json', 'apikey': self.api_key}
        return super(KanbanizeSession, self).request(method, url=self.uri + url, data=data, headers=headers, **kwargs)

    def send(self, request, **kwargs):
        r = super().send(request, **kwargs)
        return self.__middleware_response(r)

    @staticmethod
    def __middleware_response(r: Response) -> Any:
        status_message = {
            500: {'code': 500, 'message': 'The request failed due to an internal server error.'},
            503: {'code': 503, 'message': 'The service is temporarily unavailable.'},
            0: 'There was an unexpected error when making the request.'
        }

        if r.status_code in [200, 204]:
            response = json.loads(r.content) if r.status_code == 200 else None
            return response.get('data') if response else None

        response = json.loads(r.content) \
            if r.status_code in [400, 401, 403, 404, 409, 429] else status_message.get(r.status_code)

        raise ValueError(
            response.get('error') if response else {'code': r.status_code, 'message': status_message.get(0)}
        )
