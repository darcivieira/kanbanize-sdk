from kanbanize_sdk import Kanbanize, WorkspacesInsertBody, WorkspacesUpdateBody


def test_list_workspaces(requests_mock):
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
    requests_mock.get('https://teste.kanbanize.com/api/v2/workspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspaces().list() == test_json.get('data')

def test_insert_workspaces(requests_mock):
    test_json = {
        "data": {
            "workspace_id": 0,
            "type": 1,
            "is_archived": 0,
            "name": "teste"
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/workspaces', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = WorkspacesInsertBody(name='teste', _type=1)
    assert service.workspaces().insert(body) == test_json.get('data')

def test_get_workspaces(requests_mock):
    test_json = {
        "data": 
            {
                "type": 1,
                "is_archived": 0,
                "name": "teste"
            }
        
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/workspaces/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workspaces().get(workspace_id=1) == test_json.get('data')

def test_update_workspaces(requests_mock):
    test_json = {
        "data":
        {
            "type": 1,
            "is_archived": 0,
            "name": "teste1541"
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/workspaces/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = WorkspacesUpdateBody(name='teste', is_archived=1)
    assert service.workspaces().update(1, body) == test_json.get('data')