from pytest import mark
from kanbanize_sdk import Kanbanize, BoardSettingsUpdateBody


@mark.board_settings
def test_get_board_settings(requests_mock):
    test_json = {
        'data': {
            'size_type': 0,
            'allow_exceeding': 0,
            'autoarchive_cards_after': 7,
            'limit_type': 0,
            'allow_repeating_custom_card_ids': 0,
            'is_discard_reason_required': 0,
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/settings', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.board_settings().get(board_id=1) == test_json.get('data')


@mark.board_settings
def test_update_board_settings(requests_mock):
    test_json = {
        'data': {
            'size_type': 0,
            'allow_exceeding': 0,
            'autoarchive_cards_after': 7,
            'limit_type': 0,
            'allow_repeating_custom_card_ids': 0,
            'is_discard_reason_required': 0,
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1/settings', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = BoardSettingsUpdateBody(size_type=0)
    assert service.board_settings().update(1, body) == test_json.get('data')
