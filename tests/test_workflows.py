from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.workflows
def test_list_workflows(requests_mock):
    test_json = {
        'data': {
            'workflow_id': 0,
            'type': 0,
            'position': 0,
            'is_enabled': 0,
            'is_collapsible': 0,
            'name': 'Test',
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/workflows', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().list(board_id=1) == test_json.get('data')
