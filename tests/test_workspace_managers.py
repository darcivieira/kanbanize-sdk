from kanbanize_sdk import Kanbanize
from pytest import mark

@mark.workspace_managers
def test_list_workspace_managers(httpx_mock):
    test_json = {
         "data": [
                {
                "manager_id": 2
                }
            ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/workspaces/1/managers', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().list(workspace_id=1) == test_json.get('data')

@mark.workspace_managers
def test_get_workspace_managers(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().get(workspace_id=1, user_id=2) == None

@mark.workspace_managers
def test_put_workspace_managers(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().update(workspace_id=1, user_id=2) == None

@mark.workspace_managers
def test_delete_workspace_managers(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/workspaces/1/managers/2', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspace_managers().delete(workspace_id=1, user_id=2, ) == None