from kanbanize_sdk import Kanbanize
from pytest import mark

@mark.managed_workspaces
def test_list_managed_workspaces(httpx_mock):
    test_json = {
        "data": [
            {
                'workspace_id': 1,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/users/1/managedWorkspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.managed_workspaces().list(user_id=1) == test_json.get('data')
