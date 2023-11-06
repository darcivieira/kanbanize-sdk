from pytest import mark
from kanbanize_sdk import Kanbanize, ColumnsInsertBody


@mark.columns
def test_list_columns(requests_mock):
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
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/columns', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.columns().list(board_id=1) == test_json.get('data')


@mark.columns
def test_inset_columns(requests_mock):
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
    requests_mock.post('https://teste.kanbanize.com/api/v2/boards/1/columns', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = ColumnsInsertBody(
        workflow_id=1, section=1, parent_column_id=1, position=1, name='Test', limit=0, cards_per_row=0, flow_type=0
    )
    assert service.columns().insert(board_id=1, body=body) == test_json.get('data')
