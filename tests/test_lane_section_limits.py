from pytest import mark

from kanbanize_sdk import Kanbanize, LaneSectionLimitsUpdateBody


@mark.lane_section_limits
def test_list_lane_section_limits(httpx_mock):
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
    httpx_mock.add_response(method='GET', url='https://test.kanbanize.com/api/v2/boards/1/laneSectionLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'api_key': 'token'})
    assert service.lane_section_limits().list(board_id=1) == test_json.get('data')


@mark.lane_section_limits
def test_update_lane_section_limits(httpx_mock, assert_json_body):
    test_json = {
        'data': {
            "board_id": 0,
            "lane_id": 0,
            "section": 0,
            "limit": 0
        }
    }
    httpx_mock.add_response(method='PUT', url='https://test.kanbanize.com/api/v2/boards/1/laneSectionLimits', json=test_json)
    service = Kanbanize({'subdomain': 'test', 'api_key': 'token'})
    body = LaneSectionLimitsUpdateBody(lane_id=1, section=1, limit=1000)
    assert service.lane_section_limits().update(board_id=1, body=body) == test_json.get('data')
    assert_json_body(body.to_dict())
