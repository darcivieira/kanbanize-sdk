from kanbanize_sdk import Kanbanize


def test_get_workspaces_managers(requests_mock):
    test_json = {
         "data": [
                {
                "manager_id": 2
                }
            ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/workspaces/1/managers/56', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().list(workspace_id=1, user_id=2) == test_json.get('data')

def test_get_workspaces_managers(requests_mock):
    requests_mock.get('https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().get(workspace_id=1, user_id=2) == None

def test_put_workspaces_managers(requests_mock):
    requests_mock.put('https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().update(workspace_id=1, user_id=2) == None

def test_delete_workspaces_managers(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().delete(workspace_id=1, user_id=2, ) == None