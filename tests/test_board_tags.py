from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_tags
def test_list_board_tags(httpx_mock):
    test_json = {
        'data': [
            {
                "tag_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/tags', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_tags().list(board_id=1) == test_json.get('data')


@mark.board_tags
def test_get_board_tags(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/tags/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_tags().get(1, 1) is None


@mark.board_tags
def test_update_board_tags(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/tags/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_tags().update(1, 1) is None


@mark.board_tags
def test_delete_board_tags(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/tags/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_tags().delete(1, 1) is None
