from pytest import mark
from kanbanize_sdk import Kanbanize, BoardsInsertBody, BoardsUpdateBody


@mark.boards
def test_list_boards(requests_mock):
    test_json = {
        'data': [
            {
                'board_id': 1,
                'workspace_id': 0,
                'is_archived': 0,
                'name': 'Teste',
                'description': 'Description teste'
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().list() == test_json.get('data')


@mark.boards
def test_get_board(requests_mock):
    test_json = {
        'data': {
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Teste',
            'description': 'Description teste'
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().get(board_id=1) == test_json.get('data')


@mark.boards
def test_insert_board(requests_mock):
    test_json = {
        'data': {
            'board_id': 1,
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Test',
            'description': 'Description test'
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardsInsertBody(workspace_id=0, name='Teste', description='Description test')
    assert service.boards().insert(body) == test_json.get('data')


@mark.boards
def test_update_board(requests_mock):
    test_json = {
        'data': {
            'board_id': 1,
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Test',
            'description': 'Description test'
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardsUpdateBody(is_archived=0)
    assert service.boards().update(1, body) == test_json.get('data')


@mark.boards
def test_delete_board(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().delete(1) is None
