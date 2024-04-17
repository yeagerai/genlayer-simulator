import json

from tests.base import (
    not_url,
    url_doesnt_exist,
    working_url,
    get_payload,
    post_request
)


def test_get_webpage_bad_url():
    payload = get_payload('get_webpage', not_url())
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL not in correct format'


def test_get_webpage_url_doesnt_exist():
    payload = get_payload('get_webpage', url_doesnt_exist())
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL does not exist'


def test_get_webpage():
    payload = get_payload('get_webpage', working_url())
    test_text = 'INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS'
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'success'
    assert test_text in response_json['result']['response']