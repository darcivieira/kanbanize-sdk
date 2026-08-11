from pytest import mark
from kanbanize_sdk import Kanbanize, WorkflowsInsetBody, WorkflowsUpdateBody, WorkflowsCopyBody


@mark.workflows
def test_list_workflows(httpx_mock):
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
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/workflows', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().list(board_id=1) == test_json.get('data')


@mark.workflows
def test_insert_workflow(httpx_mock, assert_json_body):
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
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/boards/1/workflows', json=test_json)
    body = WorkflowsInsetBody(position=0, is_enabled=0, is_collapsible=0, name='Teste', _type=0)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().insert(board_id=1, body=body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.workflows
def test_get_workflow(httpx_mock):
    test_json = {
        'data': {
            'type': 0,
            'position': 0,
            'is_enabled': 0,
            'is_collapsible': 0,
            'name': 'Test',
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/workflows/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().get(board_id=1, workflow_id=1) == test_json.get('data')


@mark.workflows
def test_update_workflow(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'type': 0,
            'position': 0,
            'is_enabled': 0,
            'is_collapsible': 0,
            'name': 'Test',
        }
    }
    httpx_mock.add_response(method='PATCH', url='https://teste.kanbanize.com/api/v2/boards/1/workflows/1', json=test_json)
    body = WorkflowsUpdateBody(position=1)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().update(board_id=1, workflow_id=1, body=body) == test_json.get('data')
    assert_json_body(body.to_dict())


@mark.workflows
def test_delete_workflow(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/workflows/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().delete(board_id=1, workflow_id=1) is None


@mark.workflows
def test_copy_workflow(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            'board_structure': {},
            'cycle_time_column_ids': [
                0
            ],
            'initiative_workflow_settings': [
                {
                    "workflow_id": 1,
                    "built_in_rules_can_start_initiatives": 0,
                    "built_in_rules_can_finish_initiatives": 0,
                    "built_in_rules_can_move_to_requested": 0,
                    "built_in_rules_can_move_back_from_done": 0,
                    "built_in_rules_can_move_from_backlog_to_requested": 0,
                }
            ]
        }
    }
    httpx_mock.add_response(method='POST', url='https://teste.kanbanize.com/api/v2/boards/1/workflows/1/copy', json=test_json)
    body = WorkflowsCopyBody(
        name="Test", to_board_id=0, copy_service_level_expectations=1, copy_column_checklist_items=1
    )
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.workflows().copy(board_id=1, workflow_id=1, body=body) == test_json.get('data')
    assert_json_body(body.to_dict())
