from pytest import mark
from kanbanize_sdk import Kanbanize, TeamsInsertBody, TeamsUpdateBody


@mark.teams
def test_list_teams(requests_mock):
    test_json = {
        'data': [
            {
                'team_id': 1,
                'name': 'Team name',
                'description': 'Team description'
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/teams', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().list() == test_json.get('data')


@mark.teams
def test_get_team(requests_mock):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/teams/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().get(team_id=1) == test_json.get('data')


@mark.teams
def test_invite_team(requests_mock):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/teams', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = TeamsInsertBody(name='Team name')
    assert service.teams().insert(body) == test_json.get('data')


@mark.teams
def test_update_team(requests_mock):
    test_json = {
        'data': {
            'team_id': 1,
            'name': 'Team name',
            'description': 'Team description'
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/teams/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = TeamsUpdateBody(description='Other team name')
    assert service.teams().update(1, body) == test_json.get('data')


@mark.teams
def test_delete_team(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/teams/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.teams().delete(1) == None
