from pytest import mark
from kanbanize_sdk import Kanbanize, BoardAssigneesUpdateBody


@mark.board_assignees
def test_list_board_assignees(requests_mock):
    test_json = {
        'data': [
            {
                "user_id": 0,
                "role_id": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/userRoles', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_assignees().list(board_id=1) == test_json.get('data')


@mark.board_assignees
def test_get_board_assignees(requests_mock):
    test_json = {
        'data': {
            "role_id": 0,
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/userRoles/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_assignees().get(board_id=1, user_id=1) == test_json.get('data')


@mark.board_assignees
def test_update_board_assignees(requests_mock):
    test_json = {
        'data': {
            "role_id": 0
        }
    }
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/userRoles/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardAssigneesUpdateBody(role_id=0)
    assert service.board_assignees().update(1, 1, body) == test_json.get('data')


@mark.board_assignees
def test_delete_board_assignees(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/userRoles/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_assignees().delete(1, 1) is None
