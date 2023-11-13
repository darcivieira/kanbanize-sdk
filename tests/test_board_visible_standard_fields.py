from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_visible_standard_fields
def test_list_board_visible_standard_fields(requests_mock):
    test_json = {
        'data': [
            {
                "board_id": 0,
                "last_modified": 0,
                "in_current_position_since": 0,
                "created_at": 0,
                "reporter": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().list(board_id=1) == test_json.get('data')


@mark.board_visible_standard_fields
def test_get_merged_area(requests_mock):
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().get(1, 1) is None


@mark.board_visible_standard_fields
def test_update_merged_area(requests_mock):
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().update(1, 1) is None


@mark.board_visible_standard_fields
def test_delete_merged_area(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/visibleStandardFields/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_visible_standard_fields().delete(1, 1) is None
