from pytest import mark
from kanbanize_sdk import Kanbanize, WorkspacesInsertBody, WorkspacesUpdateBody


@mark.workspaces
def test_list_workspaces(httpx_mock):
    test_json = {
        "data": [
            {
                'workspace_id': 0,
                "type": 1,
                "is_archived": 0,
                "name": "string"
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/workspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspaces().list() == test_json.get('data')

@mark.workspaces
def test_insert_workspaces(httpx_mock, assert_json_body):
    test_json = {
        "data": {
            "workspace_id": 0,
            "type": 1,
            "is_archived": 0,
            "name": "teste"
        }
    }
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/workspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = WorkspacesInsertBody(name='teste', type=1)
    assert service.workspaces().insert(body) == test_json.get('data')
    assert_json_body(body.to_dict())

@mark.workspaces
def test_get_workspaces(httpx_mock):
    test_json = {
        "data": 
            {
                "type": 1,
                "is_archived": 0,
                "name": "teste"
            }
        
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/workspaces/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspaces().get(workspace_id=1) == test_json.get('data')

@mark.workspaces
def test_update_workspaces(httpx_mock, assert_json_body):
    test_json = {
        "data":
        {
            "type": 1,
            "is_archived": 0,
            "name": "teste1541"
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/workspaces/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = WorkspacesUpdateBody(name='teste', is_archived=1)
    assert service.workspaces().update(1, body) == test_json.get('data')
    assert_json_body(body.to_dict())
