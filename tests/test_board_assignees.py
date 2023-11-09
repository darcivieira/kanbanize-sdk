from pytest import mark
from kanbanize_sdk import Kanbanize, MergedAreasInsertBody, MergedAreasUpdateBody


@mark.board_assignees
def test_list_merged_areas(requests_mock):
    test_json = {
        'data': [
            {
                "area_id": 0,
                "board_id": 0,
                "primary_column_id": 0,
                "limit": 0,
                "lane_ids": [
                    0
                ],
                "column_ids": [
                    0
                ]
            }
        ]
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/mergedAreas', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.merged_areas().list(board_id=1) == test_json.get('data')


@mark.board_assignees
def test_get_merged_area(requests_mock):
    test_json = {
        'data': {
            "area_id": 0,
            "board_id": 0,
            "primary_column_id": 0,
            "limit": 0,
            "lane_ids": [
                0
            ],
            "column_ids": [
                0
            ]
        }
    }
    requests_mock.get('https://teste.kanbanize.com/api/v2/boards/1/mergedAreas/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.merged_areas().get(board_id=1, area_id=1) == test_json.get('data')


@mark.board_assignees
def test_insert_merged_area(requests_mock):
    test_json = {
        'data': {
            "area_id": 0,
            "board_id": 0,
            "primary_column_id": 0,
            "limit": 0,
            "lane_ids": [
                0
            ],
            "column_ids": [
                0
            ]
        }
    }
    requests_mock.post('https://teste.kanbanize.com/api/v2/boards/1/mergedAreas', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = MergedAreasInsertBody(lane_ids=[0], column_ids=[0], primary_column_id=0, limit=0)
    assert service.merged_areas().insert(1, body) == test_json.get('data')


@mark.board_assignees
def test_update_merged_area(requests_mock):
    test_json = {
        'data': {
            "area_id": 0,
            "board_id": 0,
            "primary_column_id": 0,
            "limit": 0,
            "lane_ids": [
                0
            ],
            "column_ids": [
                0
            ]
        }
    }
    requests_mock.patch('https://teste.kanbanize.com/api/v2/boards/1/mergedAreas/1', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    body = MergedAreasUpdateBody(lane_ids=[0])
    assert service.merged_areas().update(1, 1, body) == test_json.get('data')


@mark.board_assignees
def test_delete_merged_area(requests_mock):
    requests_mock.delete('https://teste.kanbanize.com/api/v2/boards/1/mergedAreas/1', status_code=204)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.merged_areas().delete(1, 1) is None
