from kanbanize_sdk import Kanbanize, UsersInsertBody, UsersUpdateBody
from pytest import mark

@mark.users
def test_list_users(requests_mock):
    test_json = {
        'data': [
            {
                'user_id': 1,
                'email': 'teste@teste.com',
                'username': 'teste',
                'realname': 'Teste',
                'avatar': 'url.avatar',
                'is_enabled': 0,
                'is_confirmed': 0,
                'is_tfa_enabled': 0,
                'registration_date': '2023-10-24'
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/users', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.users().list() == test_json.get('data')

@mark.users
def test_get_user(requests_mock):
    test_json = {
        'data': {
            'user_id': 1,
            'email': 'teste@teste.com',
            'username': 'teste',
            'realname': 'Teste',
            'avatar': 'url.avatar',
            'is_enabled': 0,
            'is_confirmed': 0,
            'is_tfa_enabled': 0,
            'registration_date': '2023-10-24'
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/users/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.users().get(user_id=1) == test_json.get('data')

@mark.users
def test_invite_user(requests_mock):
    test_json = {
        'data': {
            'user_id': 1,
            'email': 'teste@teste123.com',
            'username': 'teste',
            'realname': 'Teste',
            'avatar': 'url.avatar',
            'is_enabled': 0,
            'is_confirmed': 0,
            'is_tfa_enabled': 0,
            'registration_date': '2023-10-24'
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/users', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = UsersInsertBody(email='teste@teste.com')
    assert service.users().insert(body) == test_json.get('data')

@mark.users
def test_update_user(requests_mock):
    test_json = {
        'data': {
            'user_id': 1,
            'email': 'teste@teste.com',
            'username': 'teste',
            'realname': 'Teste',
            'avatar': 'url.avatar',
            'is_enabled': 0,
            'is_confirmed': 0,
            'is_tfa_enabled': 0,
            'registration_date': '2023-10-24'
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/users/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = UsersUpdateBody(is_enabled=1)
    assert service.users().update(1, body) == test_json.get('data')

@mark.users
def test_delete_user(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/users/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.users().delete(1) == None
