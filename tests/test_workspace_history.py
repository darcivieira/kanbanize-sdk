from kanbanize_sdk import Kanbanize
from pytest import mark


@mark.workspaces_history
def test_list_workspaces_history(httpx_mock):
    test_json = {
        'pagination': {
            'all_pages': 0,
            'current_page': 0,
            'results_per_page': 0
        },
        "data": [
            {
                "history_id": 0,
                "workspace_id": 0,
                "event_type": "teste",
                "user_id": 0,
                "details": {},
                "time": "2023-11-01"
            }
        ]
    }
    response = {
        'all_pages': 0,
        'current_page': 0,
        'results_per_page': 0,
        "data": [
            {
                "history_id": 0,
                "workspace_id": 0,
                "event_type": "teste",
                "user_id": 0,
                "details": {},
                "time": "2023-11-01"
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/workspaces/history', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_history().list() == response
