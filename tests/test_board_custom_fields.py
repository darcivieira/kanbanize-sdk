from pytest import mark
from kanbanize_sdk import Kanbanize, BoardCustomFieldsInsertBody, BoardCustomFieldsUpdateBody


@mark.board_custom_fields
def test_list_board_custom_fields(requests_mock):
    test_json = {
        'data': [
            {
                "field_id": 0,
                "position": 0,
                "color": 'ffffff',
                "is_always_present": 0,
                "display_width": 0,
                "prefix": 0,
                "suffix": 0,
                "unique_values": 0,
                "value_is_required": 0,
                "default_value": 0,
                "inherit_default_value": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/customFields', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_fields().list(board_id=1) == test_json.get('data')


@mark.board_custom_fields
def test_get_board_custom_fields(requests_mock):
    test_json = {
        'data': {
            "position": 0,
            "color": 'ffffff',
            "is_always_present": 0,
            "display_width": 0,
            "prefix": 0,
            "suffix": 0,
            "unique_values": 0,
            "value_is_required": 0,
            "default_value": 0,
            "inherit_default_value": 0,
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/customFields/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_fields().get(board_id=1, field_id=1) == test_json.get('data')


@mark.board_custom_fields
def test_insert_board_custom_fields(requests_mock):
    test_json = {
        'data': {
            "position": 0,
            "color": 'ffffff',
            "is_always_present": 0,
            "display_width": 0,
            "prefix": 0,
            "suffix": 0,
            "unique_values": 0,
            "value_is_required": 0,
            "default_value": 0,
            "inherit_default_value": 0,
        }
    }
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/customFields/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCustomFieldsInsertBody(
        is_always_present=0,
        position=0,
        display_width=1,
        prefix='test',
        suffix='test',
        unique_values=0,
        value_is_required=0,
        default_value='test',
        inherit_default_value=0
    )
    assert service.board_custom_fields().insert(board_id=1, field_id=1, body=body) == test_json.get('data')


@mark.board_custom_fields
def test_update_board_custom_fields(requests_mock):
    test_json = {
        'data': {
            "position": 0,
            "color": 'ffffff',
            "is_always_present": 0,
            "display_width": 0,
            "prefix": 0,
            "suffix": 0,
            "unique_values": 0,
            "value_is_required": 0,
            "default_value": 0,
            "inherit_default_value": 0,
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1/customFields/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardCustomFieldsUpdateBody(is_always_present=0)
    assert service.board_custom_fields().update(1, 1, body) == test_json.get('data')


@mark.board_custom_fields
def test_delete_board_custom_fields(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/customFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_fields().delete(1, 1) is None
