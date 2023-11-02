from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_structure
def test_get_board_structure(requests_mock):
    test_json = {
        'data': {}
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/currentStructure', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_structure().get(board_id=1) == test_json.get('data')


@mark.board_structure
def test_get_board_structure_revisions(requests_mock):
    test_json = {
        'data': {
            'role_id': 0
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/currentStructure/revision', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_structure().get_revision(board_id=1) == test_json.get('data')
