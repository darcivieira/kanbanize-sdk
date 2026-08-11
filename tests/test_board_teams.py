from pytest import mark
from kanbanize_sdk import Kanbanize, BoardTeamsUpdateBody


@mark.board_teams
def test_list_board_teams(httpx_mock):
    test_json = {
        'data': [
            {
                "team_id": 0,
                "role_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/teams', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_teams().list(board_id=1) == test_json.get('data')


@mark.board_teams
def test_get_board_teams(httpx_mock):
    test_json = {
        'data': [
            {
                "team_id": 0,
                "role_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/teams/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_teams().get(1, 1) is None


@mark.board_teams
def test_update_board_teams(httpx_mock, assert_json_body):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/teams/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardTeamsUpdateBody(role_id=0)
    assert service.board_teams().update(1, 1, body) is None
    assert_json_body(body.to_dict())


@mark.board_teams
def test_delete_board_teams(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/teams/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_teams().delete(1, 1) is None
