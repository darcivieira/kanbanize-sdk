import json

from pytest import fixture


@fixture
def assert_json_body(httpx_mock):
    """
    Asserts that the last captured request carried `expected` as a JSON body.

    The SDK always announces Content-Type: application/json, so a body encoded as
    application/x-www-form-urlencoded is a defect even when the server tolerates it. This
    helper fails loudly on that case instead of letting a form-encoded body pass unnoticed —
    see tests/test_wrapper.py for the test that proves it does.
    """

    def _assert(expected: dict):
        request = httpx_mock.get_request()
        assert request is not None, 'no request was captured'

        try:
            sent = json.loads(request.content)
        except json.JSONDecodeError:
            raise AssertionError(
                'body is not JSON. '
                f"content-type={request.headers.get('content-type')!r} "
                f'content={request.content!r}'
            ) from None

        assert sent == expected

    return _assert
