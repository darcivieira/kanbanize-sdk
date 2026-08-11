from pytest import mark
from kanbanize_sdk import Kanbanize, TeamsInsertBody, TeamsUpdateBody


@mark.teams
def test_list_teams(httpx_mock):
    test_json = {
        'data': [
            {
                'team_id': 1,
                'name': 'Team name',
                'description': 'Team description'
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/teams', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().list() == test_json.get('data')


@mark.teams
def test_get_team(httpx_mock):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/teams/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().get(team_id=1) == test_json.get('data')


@mark.teams
def test_invite_team(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/teams', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = TeamsInsertBody(name='Team name')
    assert service.teams().insert(body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.teams
def test_update_team(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/teams/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = TeamsUpdateBody(description='Other team name')
    assert service.teams().update(1, body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.teams
def test_delete_team(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/teams/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().delete(1) is None
