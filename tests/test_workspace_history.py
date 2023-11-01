from kanbanize_sdk import Kanbanize


def test_list_workspaces_history(requests_mock):
    test_json = {
        "pagination": {
            "all_pages": 1,
            "current_page": 1,
            "results_per_page": 10
        },
        "data": [
            {
            "history_id": 0,
            "workspace_id": 0,
            "event_type": "string",
            "user_id": 0,
            "details": {},
            "time": "2023-11-01"
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/workspaces/history', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_history().list() == test_json.get('data')