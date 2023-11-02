from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_history
def test_list_board_history(requests_mock):
    test_json = {
        'pagination': {
          'all_pages': 0,
          'current_page': 0,
          'results_per_page': 0
        },
        'data': [
            {
                'history_id': 0,
                'board_id': 0,
                'event_type': 'teste',
                'user_id': 0,
                'details': {},
                'time': '2023-11-02',
            }
        ]
    }
    response = {
        'all_pages': 0,
        'current_page': 0,
        'results_per_page': 0,
        'data': [
            {
                'history_id': 0,
                'board_id': 0,
                'event_type': 'teste',
                'user_id': 0,
                'details': {},
                'time': '2023-11-02',
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/history', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    aaa = service.board_history().list()
    print(aaa)
    assert service.board_history().list() == response
