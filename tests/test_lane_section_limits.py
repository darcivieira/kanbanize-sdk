from pytest import mark

from kanbanize_sdk import Kanbanize, CellLimitsUpdateBody


@mark.lane_section_limits
def test_list_lane_section_limits(requests_mock):
    test_json = {
        'data': [
            {
                "board_id": 0,
                "lane_id": 0,
                "section": 0,
                "limit": 0
            }
        ]
    }
    requests_mock.get('https://test.kanbanize.com/api/v2/boards/1/laneSectionLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'apy_key': 'token'})
    assert service.lane_section_limits().list(board_id=1) == test_json.get('data')


@mark.lane_section_limits
def test_update_lane_section_limits(requests_mock):
    test_json = {
        'data': {
            "board_id": 0,
            "lane_id": 0,
            "section": 0,
            "limit": 0
        }
    }
    requests_mock.put('https://test.kanbanize.com/api/v2/boards/1/laneSectionLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'apy_key': 'token'})
    body = CellLimitsUpdateBody(lane_id=1, column_id=1, limit=1000)
    assert service.lane_section_limits().update(board_id=1, body=body) == test_json.get('data')
