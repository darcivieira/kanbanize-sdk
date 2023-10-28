from kanbanize_sdk import Kanbanize


def test_list_managed_workspaces(requests_mock):
    test_json = {
        "data": [
            {
                'workspace_id': 1,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/users/1/managedWorkspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.managedWorkspace().list(user_id=1) == test_json.get('data')
