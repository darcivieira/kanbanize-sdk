
from kanbanize_sdk import kanbanize


def test_list_users(requests_mock):
    service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    test_json = [{'user_id': 1, 'email': 'teste@teste.com'}]
    requests_mock.get('https://teste.kanbanize.com/api/v2/users', json=test_json)
    assert service.users().list().json() == test_json


def test_get_user(requests_mock):
    service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    test_json = [{'user_id': 1, 'email': 'teste@teste.com'}]
    requests_mock.get('https://teste.kanbanize.com/api/v2/users', json=test_json)
    assert service.users().list().json() == test_json


def test_invite_user(requests_mock):
    service = kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    test_json = [{'user_id': 1, 'email': 'teste@teste.com'}]
    requests_mock.get('https://teste.kanbanize.com/api/v2/users', json=test_json)
    assert service.users().list().json() == test_json
