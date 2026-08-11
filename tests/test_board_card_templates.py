from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.board_card_templates
def test_list_board_card_templates(httpx_mock):
    test_json = {
        'data': [
            {
                "template_id": 0,
            }
        ]
    }
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/cardTemplates', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().list(board_id=1) == test_json.get('data')


@mark.board_card_templates
def test_get_board_card_template(httpx_mock):
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().get(1, 1) is None


@mark.board_card_templates
def test_update_board_card_template(httpx_mock):
    httpx_mock.add_response(method='PUT', url='https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().update(1, 1) is None


@mark.board_card_templates
def test_delete_board_card_template(httpx_mock):
    httpx_mock.add_response(method='DELETE', url='https://teste.kanbanize.com/api/v2/boards/1/cardTemplates/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_card_templates().delete(1, 1) is None
