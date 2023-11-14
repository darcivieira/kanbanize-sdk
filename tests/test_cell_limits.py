from pytest import mark

from kanbanize_sdk import Kanbanize, CellLimitsUpdateBody


@mark.cell_limits
def test_list_cell_limits(requests_mock):
    test_json = {
        'data': [
            {
                'board_id': 0,
                'lane_id': 0,
                'column_id': 0,
                'limit': 0
            }
        ]
    }
    requests_mock.get('https://test.kanbanize.com/api/v2/boards/1/cellLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'apy_key': 'token'})
    assert service.cell_limits().list(board_id=1) == test_json.get('data')


@mark.cell_limits
def test_update_cell_limits(requests_mock):
    test_json = {
        'data': {
            'board_id': 0,
            'lane_id': 0,
            'column_id': 0,
            'limit': 1000
        }
    }
    requests_mock.put('https://test.kanbanize.com/api/v2/boards/1/cellLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'apy_key': 'token'})
    body = CellLimitsUpdateBody(lane_id=1, column_id=1, limit=1000)
    assert service.cell_limits().update(board_id=1, body=body) == test_json.get('data')
