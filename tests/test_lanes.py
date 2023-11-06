from pytest import mark
from kanbanize_sdk import Kanbanize, LanesInsertBody, LanesUpdateBody


@mark.lanes
def test_list_lanes(requests_mock):
    test_json = {
        'data': [
            {
                'lane_id': 1,
                'workflow': 0,
                'parent_lane_id': 0,
                'position': 0,
                'name': 'Teste',
                'description': 'Description teste',
                'color': 'ffffff',
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/lanes', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.lanes().list(board_id=1) == test_json.get('data')


@mark.lanes
def test_get_lane(requests_mock):
    test_json = {
        'data': {
            'workflow': 0,
            'parent_lane_id': 0,
            'position': 0,
            'name': 'Teste',
            'description': 'Description teste',
            'color': 'ffffff',
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/lanes/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.lanes().get(board_id=1, lane_id=1) == test_json.get('data')


@mark.lanes
def test_insert_lane(requests_mock):
    test_json = {
        'data': {
            'lane_id': 1,
            'workflow': 1,
            'parent_lane_id': 0,
            'position': 0,
            'name': 'Test',
            'description': 'Description test',
            'color': 'ffffff',
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/boards/1/lanes', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = LanesInsertBody(workflow_id=1, parent_lane_id=1, position=0, name='Test', description='Test', color='ffffff')
    assert service.lanes().insert(1, body) == test_json.get('data')


@mark.lanes
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
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1/lanes/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = LanesUpdateBody(position=1)
    assert service.lanes().update(1, 1, body) == test_json.get('data')


@mark.lanes
def test_delete_board(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/lanes/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.lanes().delete(1, 1) is None
