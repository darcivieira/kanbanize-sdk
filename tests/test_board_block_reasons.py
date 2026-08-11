from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_block_reasons
def test_list_board_block_reasons(httpx_mock):
    test_json = {
        'data': [
            {
                "reason_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/blockReasons', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_block_reasons().list(board_id=1) == test_json.get('data')


@mark.board_block_reasons
def test_get_board_block_reason(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/blockReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_block_reasons().get(1, 1) is None


@mark.board_block_reasons
def test_update_board_block_reason(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/blockReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_block_reasons().update(1, 1) is None


@mark.board_block_reasons
def test_delete_board_block_reason(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/blockReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_block_reasons().delete(1, 1) is None
