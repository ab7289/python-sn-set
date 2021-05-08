from unittest import mock

import pytest
from requests.exceptions import HTTPError

from sn_set.requests_lib import make_request


def test_make_request_valid(requests_mock, mock_env_vars):
    mock_response = {
        "result": [
            {
                "name": "some update set",
                "state": "complete",
                "description": "some desc",
                "sys_created_by": "ab7289",
                "sys_created_on": "2021-05-05 12:12:12",
                "sys_updated_on": "2021-05-05 12:12:12",
                "sys_id": "123456789",
            }
        ]
    }
    mock_uri = (
        "https://nyudev.service-now.com/api/now/table/"
        "sys_update_set?sysparm_query=state%3Dcomplete%5Esys_idIN12345&sysparm_limit=1"
    )
    test_uri = "https://nyudev.service-now.com/api/now/table/sys_update_set"
    test_params = {"sysparm_query": "state=complete^sys_idIN12345", "sysparm_limit": 1}
    valid_response = [
        {
            "name": "some update set",
            "state": "complete",
            "description": "some desc",
            "sys_created_by": "ab7289",
            "sys_created_on": "2021-05-05 12:12:12",
            "sys_updated_on": "2021-05-05 12:12:12",
            "sys_id": "123456789",
        }
    ]
    requests_mock.get(mock_uri, json=mock_response, status_code=200)
    r = make_request(test_uri, path_params=test_params)
    assert r == valid_response


def test_make_request_unauthorized(requests_mock, mock_env_vars):
    mock_uri = "mock://some-test.com"
    requests_mock.get(mock_uri, status_code=401)
    with pytest.raises(HTTPError):
        make_request(mock_uri)


def test_make_request_not_found(requests_mock, mock_env_vars):
    mock_uri = "mock://some-test.com"
    requests_mock.get(mock_uri, status_code=404)
    with pytest.raises(HTTPError):
        make_request(mock_uri)


def test_make_request_no_data(requests_mock, mock_env_vars):
    mock_uri = "mock://some-test.com"
    mock_response = {"result": []}

    requests_mock.get(mock_uri, json=mock_response, status_code=200)
    r = make_request(mock_uri)
    assert r == []


def test_make_request_missing_pass(requests_mock, mock_empty_env_vars):
    mock_uri = "mock://some-test.com"
    with pytest.raises(ValueError):
        make_request(mock_uri)


def test_get_update_sets_valid(monkeypatch):

    mock_payload = [{"name": "an update set", "sys_id": "12345"}]

    def mock_make_request(instance_name, path_params):
        return mock_payload

    from sn_set import requests_lib

    monkeypatch.setattr(requests_lib, "make_request", mock_make_request)
    r = requests_lib.get_update_sets("nyudev")
    assert r == mock_payload


def test_get_update_set_invalid(monkeypatch):
    from sn_set.requests_lib import get_update_sets

    with pytest.raises(ValueError):
        get_update_sets("invalid instance")


def test_get_install_order_valid(monkeypatch):
    mock_payload = [{"name": "an update set", "sys_id": "12345"}]

    def mock_make_request(instance_name, path_params):
        return mock_payload

    from sn_set import requests_lib

    monkeypatch.setattr(requests_lib, "get_install_order", mock_make_request)
    r = requests_lib.get_install_order("nyudev", ["12345"])
    assert r == mock_payload


def test_get_install_order_invalid():
    from sn_set.requests_lib import get_install_order

    with pytest.raises(ValueError):
        get_install_order("invalid_isntance", [])


@mock.patch("sn_set.requests_lib.make_request")
def test_get_install_order_400(mock_make_request):
    mock_payload = [{"name": "a set", "commit_date": "2021-05-08 18:39:00"}]
    mock_uri = "https://nyudev.service-now.com/api/now/table/sys_remote_update_set"
    test_fields = [
        "name",
        "state",
        "update_source",
        "description",
        "sys_created_on",
        "commit_date",
        "sys_updated_by",
        "sys_updated_on",
        "collisions",
    ]
    mock_params1 = {
        "sysparm_query": (
            "state=committed^nameINa,b" "^commit_dateISNOTEMPTY^ORDERBYcommit_date"
        ),
        "sysparm_fields": ",".join(test_fields),
        "sysparm_display_value": "true",
    }
    mock_params2 = {
        "sysparm_query": (
            "state=committed^name=a^commit_dateISNOTEMPTY^ORDERBYcommit_date"
        ),
        "sysparm_fields": ",".join(test_fields),
        "sysparm_display_value": "true",
    }
    mock_params3 = {
        "sysparm_query": (
            "state=committed^name=b" "^commit_dateISNOTEMPTY^ORDERBYcommit_date"
        ),
        "sysparm_fields": ",".join(test_fields),
        "sysparm_display_value": "true",
    }

    mocked_error = HTTPError(response=mock.Mock(status_code=400))

    mock_make_request.side_effect = [mocked_error, mock_payload, mock_payload]

    from sn_set.requests_lib import get_install_order

    get_install_order("nyudev", ["a", "b"])
    mock_make_request.assert_any_call(mock_uri, path_params=mock_params1)
    mock_make_request.assert_any_call(mock_uri, path_params=mock_params2)
    mock_make_request.assert_any_call(mock_uri, path_params=mock_params3)


@mock.patch("sn_set.requests_lib.make_request")
def test_get_install_list_both_400(mock_make_request):
    mock_error = HTTPError(response=mock.Mock(status_code=400))
    mock_make_request.side_effect = [mock_error, mock_error]

    from sn_set.requests_lib import get_install_order

    with pytest.raises(HTTPError):
        get_install_order("nyudev", ["12345"])


@pytest.mark.parametrize("test_value", [401, 404])
@mock.patch("sn_set.requests_lib.make_request")
def test_get_install_order_40X(mock_make_request, test_value):
    mock_make_request.side_effect = HTTPError(
        response=mock.Mock(status_code=test_value)
    )

    from sn_set.requests_lib import get_install_order

    with pytest.raises(HTTPError):
        get_install_order("nyudev", ["1234"])


def test_get_install_order_succeed():
    pass


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (" nyu dev", "pass"),
        (1234, "pass"),
        (None, "error"),
        (["1234"], "pass"),
        (["123", "123"], "pass"),
        ({}, "error"),
        ("18cc3673db009bc0121325c15b9619f3", ["18cc3673db009bc0121325c15b9619f3"]),
        (["18cc3673db009bc0121325c15b9619f3"], ["18cc3673db009bc0121325c15b9619f3"]),
        (["18cc3673db009bc0121325c15b9619f3", None], "error"),
    ],
)
def test_get_install_order_invalid_ids(test_input, expected, monkeypatch):
    from sn_set import requests_lib

    if expected == "error":
        with pytest.raises(ValueError):
            requests_lib.get_install_order("nyudev", test_input)
    else:

        def mock_make_request(instance_name, path_params):
            return expected

        monkeypatch.setattr(requests_lib, "get_install_order", mock_make_request)
        r = requests_lib.get_install_order("nyudev", test_input)
        assert r == expected


def test_get_install_order_new_invalid():
    from sn_set.requests_lib import get_install_order_new

    with pytest.raises(ValueError):
        get_install_order_new("invalid-instance", [])


def test_get_install_order_new_valid(monkeypatch):
    mock_payload = [{"name": "an update set", "sys_id": "12345"}]

    def mock_make_request(instance_name, path_params):
        return mock_payload

    from sn_set import requests_lib

    monkeypatch.setattr(requests_lib, "get_install_order_new", mock_make_request)

    assert requests_lib.get_install_order_new("nyudev", ["12345"]) == mock_payload


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (" nyu dev", "pass"),
        (1234, "pass"),
        (None, "error"),
        (["1234"], "pass"),
        (["123", "123"], "pass"),
        ({}, "error"),
        ("18cc3673db009bc0121325c15b9619f3", ["18cc3673db009bc0121325c15b9619f3"]),
        (["18cc3673db009bc0121325c15b9619f3"], ["18cc3673db009bc0121325c15b9619f3"]),
        (["18cc3673db009bc0121325c15b9619f3", None], "error"),
    ],
)
def test_get_install_order_new_invalid_ids(test_input, expected, monkeypatch):
    from sn_set import requests_lib

    if expected == "error":
        with pytest.raises(ValueError):
            requests_lib.get_install_order_new("nyudev", test_input)
    else:

        def mock_make_request(instance_name, path_params):
            return expected

        monkeypatch.setattr(requests_lib, "get_install_order_new", mock_make_request)
        r = requests_lib.get_install_order_new("nyudev", test_input)
        assert r == expected
