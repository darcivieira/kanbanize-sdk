from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_discard_reasons
def test_list_board_discard_reasons(httpx_mock):
    test_json = {
        'data': [
            {
                "reason_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/discardReasons', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().list(board_id=1) == test_json.get('data')


@mark.board_discard_reasons
def test_get_board_discard_reason(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().get(1, 1) is None


@mark.board_discard_reasons
def test_update_board_discard_reason(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().update(1, 1) is None


@mark.board_discard_reasons
def test_delete_board_discard_reason(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().delete(1, 1) is None
