import json

from tests.base import get_payload, post_request


def test_get_webpage_bad_url():
    url = '<this_is_not_a_URL>'
    payload = get_payload('get_webpage', url)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL not in correct format'


def test_get_webpage_url_doesnt_exist():
    url = 'http://www.urlthatdoesntexist.com/'
    payload = get_payload('get_webpage', url)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL does not exist'


def test_get_webpage():
    url = 'https://docs.python.org/3/license.html'
    payload = get_payload('get_webpage', url)
    test_text = 'INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS'
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'success'
    assert test_text in response_json['result']['response']