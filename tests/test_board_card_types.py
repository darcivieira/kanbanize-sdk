from pytest import mark
from kanbanize_sdk import Kanbanize, BoardCardTypesInsertBody, BoardCardTypesUpdateBody


@mark.board_card_types
def test_list_board_card_types(requests_mock):
    test_json = {
        'data': [
            {
                "type_id": 0,
                "icon_type": 0,
                "icon_id": 0,
                "color": 'text',
                "card_color_sync": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/cardTypes', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_types().list(board_id=1) == test_json.get('data')


@mark.board_card_types
def test_get_board_card_types(requests_mock):
    test_json = {
        'data': {
            "icon_type": 0,
            "icon_id": 0,
            "color": 'text',
            "card_color_sync": 0,
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/cardTypes/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_types().get(board_id=1, type_id=1) == test_json.get('data')


@mark.board_card_types
def test_get_board_card_types_settings(requests_mock):
    test_json = {
        'data': {
            "icon_type": 0,
            "icon_id": 0,
            "color": 'text',
            "card_color_sync": 0,
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/cardTypes/1/effectiveSettings', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_types().get_effective_settings(board_id=1, type_id=1) == test_json.get('data')


@mark.board_card_types
def test_insert_board_card_types(requests_mock):
    test_json = {
        'data': {
            "limit_per_board": 0,
            "limit_per_card": 0,
        }
    }
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/cardTypes/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCardTypesInsertBody(icon_type=0, icon_id=0, color='ffffff', card_color_sync=0)
    assert service.board_card_types().insert(board_id=1, type_id=1, body=body) == test_json.get('data')


@mark.board_card_types
def test_update_board_card_types(requests_mock):
    test_json = {
        'data': {
            "limit_per_board": 0,
            "limit_per_card": 0,
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1/cardTypes/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCardTypesUpdateBody(card_color_sync=0)
    assert service.board_card_types().update(1, 1, body) == test_json.get('data')


@mark.board_card_types
def test_delete_board_card_types(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/cardTypes/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_types().delete(1, 1) is None
