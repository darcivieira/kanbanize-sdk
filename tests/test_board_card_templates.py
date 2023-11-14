from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_card_templates
def test_list_board_card_templates(requests_mock):
    test_json = {
        'data': [
            {
                "template_id": 0,
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/cardTemplates', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().list(board_id=1) == test_json.get('data')


@mark.board_card_templates
def test_get_merged_area(requests_mock):
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().get(1, 1) is None


@mark.board_card_templates
def test_update_merged_area(requests_mock):
    requests_mock.put('https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().update(1, 1) is None


@mark.board_card_templates
def test_delete_merged_area(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().delete(1, 1) is None
