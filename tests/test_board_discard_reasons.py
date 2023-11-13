from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_discard_reasons
def test_list_board_discard_reasons(requests_mock):
    test_json = {
        'data': [
            {
                "reason_id": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/discardReasons', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().list(board_id=1) == test_json.get('data')


@mark.board_discard_reasons
def test_get_merged_area(requests_mock):
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().get(1, 1) is None


@mark.board_discard_reasons
def test_update_merged_area(requests_mock):
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().update(1, 1) is None


@mark.board_discard_reasons
def test_delete_merged_area(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/discardReasons/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_discard_reasons().delete(1, 1) is None
