from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_visible_standard_fields
def test_list_board_visible_standard_fields(httpx_mock):
    test_json = {
        'data': [
            {
                "board_id": 0,
                "last_modified": 0,
                "in_current_position_since": 0,
                "created_at": 0,
                "reporter": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().list(board_id=1) == test_json.get('data')


@mark.board_visible_standard_fields
def test_get_visible_standard_fields(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().get(1, 1) is None


@mark.board_visible_standard_fields
def test_update_visible_standard_fields(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().update(1, 1) is None


@mark.board_visible_standard_fields
def test_delete_visible_standard_fields(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().delete(1, 1) is None
