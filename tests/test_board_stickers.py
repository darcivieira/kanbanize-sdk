from pytest import mark
from kanbanize_sdk import Kanbanize, BoardStickersInsertBody, BoardStickersUpdateBody


@mark.board_stickers
def test_list_board_stickers(httpx_mock):
    test_json = {
        'data': [
            {
                "sticker_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/stickers', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_stickers().list(board_id=1) == test_json.get('data')


@mark.board_stickers
def test_get_board_stickers(httpx_mock):
    test_json = {
        'data': {
            "limit_per_board": 0,
            "limit_per_card": 0,
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/stickers/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_stickers().get(board_id=1, sticker_id=1) == test_json.get('data')


@mark.board_stickers
def test_insert_board_stickers(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            "limit_per_board": 0,
            "limit_per_card": 0,
        }
    }
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/stickers/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardStickersInsertBody(limit_per_board=0, limit_per_card=0)
    assert service.board_stickers().insert(board_id=1, sticker_id=1, body=body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.board_stickers
def test_update_board_stickers(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            "limit_per_board": 0,
            "limit_per_card": 0,
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/boards/1/stickers/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardStickersUpdateBody(limit_per_board=0)
    assert service.board_stickers().update(1, 1, body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.board_stickers
def test_delete_board_stickers(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/stickers/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_stickers().delete(1, 1) is None
