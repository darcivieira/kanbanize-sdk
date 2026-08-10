from pytest import mark
from kanbanize_sdk import Kanbanize, BoardCustomFieldAllowedValuesInsertBody, BoardCustomFieldAllowedValuesUpdateBody


@mark.board_custom_field_default_contributors
def test_list_board_custom_field_default_contributors(httpx_mock):
    test_json = {
        'data': [
            {
                "user_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/customFields/1/defaultContributors', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_default_contributors().list(board_id=1, field_id=1) == test_json.get('data')


@mark.board_custom_field_default_contributors
def test_get_board_custom_field_default_contributors(httpx_mock):
    httpx_mock.add_response(method='GET', url=
        'https://teste.kanbanize.com/api/v2/boards/1/customFields/1/defaultContributors/1', status_code=204
    )
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_default_contributors().get(1, 1, 1) is None


@mark.board_custom_field_default_contributors
def test_update_board_custom_field_default_contributors(httpx_mock):
    test_json = {
        'data': {
            "position": 0,
            "is_default": 0
        }
    }
    httpx_mock.add_response(method='PUT', url=
        'https://teste.kanbanize.com/api/v2/boards/1/customFields/1/defaultContributors/1', status_code=204
    )
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_default_contributors().update(1, 1, 1) is None


@mark.board_custom_field_default_contributors
def test_delete_board_custom_field_default_contributors(httpx_mock):
    httpx_mock.add_response(method='DELETE', url=
        'https://teste.kanbanize.com/api/v2/boards/1/customFields/1/defaultContributors/1', status_code=204
    )
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_custom_field_default_contributors().delete(1, 1, 1) is None
