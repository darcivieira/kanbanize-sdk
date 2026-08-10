from pytest import mark
from kanbanize_sdk import Kanbanize, ColumnsInsertBody, ColumnsUpdateBody


@mark.columns
def test_list_columns(httpx_mock):
    test_json = {
        'data': [
            {
                'column_id': 1,
                'workflow': 0,
                'section': 0,
                'parent_column_id': 0,
                'position': 0,
                'name': 'Teste',
                'description': 'Description teste',
                'color': 'ffffff',
                'limit': 0,
                'cards_per_row': 0,
                'flow_type': 1
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/columns', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.columns().list(board_id=1) == test_json.get('data')


@mark.columns
def test_inset_column(httpx_mock):
    test_json = {
        'data': {
            'column_id': 0,
            'workflow': 0,
            'section': 0,
            'parent_column_id': 0,
            'position': 0,
            'name': 'Teste',
            'description': 'Description teste',
            'color': 'ffffff',
            'limit': 0,
            'cards_per_row': 0,
            'flow_type': 1
        }
    }
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/boards/1/columns', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = ColumnsInsertBody(
        workflow_id=1, section=1, parent_column_id=1, position=1, name='Test', limit=0, cards_per_row=0, flow_type=0
    )
    assert service.columns().insert(board_id=1, body=body) == test_json.get('data')


@mark.columns
def test_get_column(httpx_mock):
    test_json = {
        'data': {
            'workflow': 0,
            'section': 0,
            'parent_column_id': 0,
            'position': 0,
            'name': 'Teste',
            'description': 'Description teste',
            'color': 'ffffff',
            'limit': 0,
            'cards_per_row': 0,
            'flow_type': 1
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/columns/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.columns().get(board_id=1, column_id=1) == test_json.get('data')


@mark.columns
def test_update_column(httpx_mock):
    test_json = {
        'data': {
            'workflow': 0,
            'section': 0,
            'parent_column_id': 0,
            'position': 0,
            'name': 'Teste',
            'description': 'Description teste',
            'color': 'ffffff',
            'limit': 0,
            'cards_per_row': 0,
            'flow_type': 1
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/boards/1/columns/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = ColumnsUpdateBody(position=2)
    assert service.columns().update(board_id=1, column_id=1, body=body) == test_json.get('data')


@mark.columns
def test_delete_column(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/columns/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.columns().delete(board_id=1, column_id=1) is None
