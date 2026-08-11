from pytest import mark
from kanbanize_sdk import Kanbanize, BoardsInsertBody, BoardsListParams, BoardsUpdateBody


@mark.boards
def test_list_boards(httpx_mock):
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
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().list() == test_json.get('data')


@mark.boards
def test_list_boards_with_params(httpx_mock):
    """`BoardsListParams` must build a usable instance and reach the wire as a query string.

    `BaseDataClasse.to_dict()` stringifies every list item, so the filters travel as repeated
    query parameters holding strings.
    """
    test_json = {
        'data': [
            {
                'board_id': 1,
                'name': 'Teste'
            }
        ]
    }
    httpx_mock.add_response(
        method='GET',
        url='https://teste.kanbanize.com/api/v2/boards'
            '?board_ids=1&board_ids=2&is_archived=0&fields=board_id&fields=name',
        json=test_json
    )
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    params = BoardsListParams(board_ids=[1, 2], is_archived=0, fields=['board_id', 'name'])

    assert params.to_dict() == {'board_ids': ['1', '2'], 'is_archived': 0, 'fields': ['board_id', 'name']}
    assert service.boards().list(params) == test_json.get('data')

    request = httpx_mock.get_request()
    assert request.url.params.get_list('board_ids') == ['1', '2']
    assert request.url.params.get_list('fields') == ['board_id', 'name']
    assert request.url.params.get('is_archived') == '0'
    assert 'workspace_ids' not in request.url.params


@mark.boards
def test_get_board(httpx_mock):
    test_json = {
        'data': {
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Teste',
            'description': 'Description teste'
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().get(board_id=1) == test_json.get('data')


@mark.boards
def test_insert_board(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'board_id': 1,
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Test',
            'description': 'Description test'
        }
    }
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardsInsertBody(workspace_id=0, name='Teste', description='Description test')
    assert service.boards().insert(body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.boards
def test_insert_board_with_a_raw_dict_body(httpx_mock, assert_json_body):
    """Every write method accepts a raw dict as well as a dataclass, and both must send JSON."""
    test_json = {'data': {'board_id': 1, 'name': 'Test'}}
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = {'workspace_id': 0, 'name': 'Teste', 'description': 'Description test'}
    assert service.boards().insert(body) == test_json.get('data')
    assert_json_body(body)


@mark.boards
def test_update_board(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'board_id': 1,
            'workspace_id': 0,
            'is_archived': 0,
            'name': 'Test',
            'description': 'Description test'
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/boards/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardsUpdateBody(is_archived=0)
    assert service.boards().update(1, body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.boards
def test_delete_board(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().delete(1) is None
