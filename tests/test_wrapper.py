import httpx
from pytest import mark, raises

from kanbanize_sdk import Kanbanize
from kanbanize_sdk.wrapper import KanbanizeSession

URL = 'https://teste.kanbanize.com/api/v2/boards/1'


def service():
    return Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})


@mark.wrapper
def test_session_does_not_inherit_from_the_http_client():
    assert httpx.Client not in KanbanizeSession.__mro__


@mark.wrapper
def test_session_exposes_uri_and_api_key():
    session = KanbanizeSession({'subdomain': 'teste', 'api_key': 'teste_key'})

    assert session.uri == 'https://teste.kanbanize.com/api/v2'
    assert session.api_key == 'teste_key'


@mark.wrapper
def test_every_request_carries_the_api_key_and_json_content_type(httpx_mock):
    httpx_mock.add_response(url=URL, json={'data': {'board_id': 1}})

    service().boards().get(1)

    request = httpx_mock.get_request()
    assert request.headers['apikey'] == 'teste_key'
    assert request.headers['content-type'] == 'application/json'


@mark.wrapper
def test_200_without_pagination_returns_only_data(httpx_mock):
    httpx_mock.add_response(url=URL, json={'data': {'board_id': 1, 'name': 'Teste'}})

    assert service().boards().get(1) == {'board_id': 1, 'name': 'Teste'}


@mark.wrapper
def test_200_with_pagination_promotes_pagination_keys_and_keeps_data(httpx_mock):
    httpx_mock.add_response(
        url=URL,
        json={
            'pagination': {'all_pages': 3, 'current_page': 1},
            'data': [{'board_id': 1}],
        },
    )

    assert service().boards().get(1) == {
        'all_pages': 3,
        'current_page': 1,
        'data': [{'board_id': 1}],
    }


@mark.wrapper
def test_204_returns_none(httpx_mock):
    httpx_mock.add_response(url=URL, method='DELETE', status_code=204)

    assert service().boards().delete(1) is None


@mark.wrapper
@mark.parametrize('status_code', [400, 401, 403, 404, 409, 429])
def test_client_errors_raise_value_error_with_the_api_error_payload(httpx_mock, status_code):
    error = {'code': status_code, 'message': 'something went wrong'}
    httpx_mock.add_response(url=URL, status_code=status_code, json={'error': error})

    with raises(ValueError) as exception:
        service().boards().get(1)

    assert exception.value.args[0] == error


@mark.wrapper
@mark.parametrize('status_code', [500, 503])
def test_server_errors_raise_value_error_with_none(httpx_mock, status_code):
    """
    Preserved behaviour, not desired behaviour.

    The status_message entry for 500 and 503 has no 'error' key, so the message is never
    delivered and callers receive ValueError(None). The requests-based implementation did
    exactly the same. Tracked as a defect in visao/ROADMAP.md.
    """
    httpx_mock.add_response(url=URL, status_code=status_code, text='')

    with raises(ValueError) as exception:
        service().boards().get(1)

    assert exception.value.args[0] is None


@mark.wrapper
@mark.parametrize('verb', ['put', 'patch'])
def test_put_and_patch_send_a_json_body(httpx_mock, assert_json_body, verb):
    httpx_mock.add_response(method=verb.upper(), url=URL, json={'data': {}})
    session = KanbanizeSession({'subdomain': 'teste', 'api_key': 'teste_key'})

    getattr(session, verb)('/boards/1', json={'name': 'Teste'})

    assert_json_body({'name': 'Teste'})


@mark.wrapper
def test_the_body_assertion_rejects_a_form_urlencoded_body(httpx_mock, assert_json_body):
    """
    Guards the guard.

    Without this, `assert_json_body` could pass for both encodings and prove nothing. Sending
    a dict through `data=` is exactly what every write method did before change 002.
    """
    httpx_mock.add_response(method='PUT', url=URL, json={'data': {}})
    session = KanbanizeSession({'subdomain': 'teste', 'api_key': 'teste_key'})

    session.put('/boards/1', data={'name': 'Teste'})

    with raises(AssertionError, match='body is not JSON'):
        assert_json_body({'name': 'Teste'})


@mark.wrapper
def test_unmapped_status_raises_value_error_with_the_generic_message(httpx_mock):
    httpx_mock.add_response(url=URL, status_code=418, text='')

    with raises(ValueError) as exception:
        service().boards().get(1)

    assert exception.value.args[0] == {
        'code': 418,
        'message': 'There was an unexpected error when making the request.',
    }
