
from kanbanize_sdk import kanbanize


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
    service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.users().list() == test_json.get('data')


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
    service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.users().get(user_id=1) == test_json.get('data')
#
#
# def test_invite_user(requests_mock):
#     service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
#     test_json = [{'user_id': 1, 'email': 'teste@teste.com'}]
#     requests_mock.get('https://teste.kanbanize.com/api/v2/users', json=test_json)
#     assert service.users().list().json() == test_json
