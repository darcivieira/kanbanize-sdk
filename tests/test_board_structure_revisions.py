from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_structure_revisions
def test_get_board_structure(httpx_mock):
    test_json = {
        'data': {
            'role_id': 0,
            'replaced_at': "2023-11-02T16:21:23.513Z"
        }
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/structureRevisions', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_structure_revisions().get(board_id=1) == test_json.get('data')


@mark.board_structure_revisions
def test_get_board_structure_revisions(httpx_mock):
    test_json = {
        'data': {}
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/structureRevisions/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_structure_revisions().get_revision(board_id=1, revision=1) == test_json.get('data')
