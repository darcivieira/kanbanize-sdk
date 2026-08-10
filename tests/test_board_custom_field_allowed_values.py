from pytest import mark
from kanbanize_sdk import Kanbanize, BoardCustomFieldAllowedValuesInsertBody, BoardCustomFieldAllowedValuesUpdateBody


@mark.board_custom_field_allowed_values
def test_list_board_custom_field_allowed_values(httpx_mock):
    test_json = {
        'data': [
            {
                "value_id": 0,
                "position": 0,
                "is_default": 0
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/allowedValues', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_allowed_values().list(board_id=1, field_id=1) == test_json.get('data')


@mark.board_custom_field_allowed_values
def test_get_board_custom_field_allowed_values(httpx_mock):
    test_json = {
        'data': {
            "position": 0,
            "is_default": 0
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/allowedValues/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_allowed_values().get(board_id=1, field_id=1, value_id=1) == test_json.get('data')


@mark.board_custom_field_allowed_values
def test_insert_board_custom_field_allowed_values(httpx_mock):
    test_json = {
        'data': {
            "position": 0,
            "is_default": 0
        }
    }
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/allowedValues/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCustomFieldAllowedValuesInsertBody(position=0, is_default=0)
    assert service.board_custom_field_allowed_values().insert(
        board_id=1, field_id=1, value_id=1, body=body) == test_json.get('data')


@mark.board_custom_field_allowed_values
def test_update_board_custom_field_allowed_values(httpx_mock):
    test_json = {
        'data': {
            "position": 0,
            "is_default": 0
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/allowedValues/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCustomFieldAllowedValuesUpdateBody(position=0)
    assert service.board_custom_field_allowed_values().update(1, 1, 1, body) == test_json.get('data')


@mark.board_custom_field_allowed_values
def test_delete_board_custom_field_allowed_values(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/allowedValues/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_allowed_values().delete(1, 1, 1) is None
