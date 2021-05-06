import pytest

from sn_set.requests_lib import (get_install_order, get_update_sets,
                                 make_request)


def test_make_request_valid(requests_mock):
    mock_response = (
        '{"result": [{"name": "some update set","state": "complete","description":'
        ' "some desc","sys_created_by": "ab7289","sys_created_on": "2021-05-05 12:12:12",'
        '"sys_updated_on": "2021-05-05 12:12:12","sys_id": "123456789"}]}'
    )
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


def test_make_request_unauthorized(requests_mock):
    mock_uri = "mock://some-test.com"
    requests_mock.get(mock_uri, status_code=401)
    with pytest.raises(ValueError):
        make_request(mock_uri)


def test_make_request_not_found(requests_mock):
    mock_uri = "mock://some-test.com"
    requests_mock.get(mock_uri, status_code=404)
    with pytest.raises(ValueError):
        make_request(mock_uri)


def test_make_request_no_data(requests_mock):
    mock_uri = "mock://some-test.com"
    mock_response = '{"result": []}'
    resp = []
    requests_mock.get(mock_uri, json=mock_response, status_code=200)
    r = make_request(mock_uri)
    assert r == []
