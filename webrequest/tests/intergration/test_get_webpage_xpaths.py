import json

from tests.base import (
    not_url,
    url_doesnt_exist,
    working_url,
    get_payload,
    post_request
)


def defaults():
    url = 'https://docs.python.org/3/license.html'
    chunck_size = 500
    overlap = 0.1
    return url, chunck_size, overlap


def test_get_webpage_xpaths_bad_url():
    _, chunk_size, overlap = defaults()
    payload = get_payload('get_webpage_chunks', not_url(), chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL not in correct format'


def test_get_webpage_url_doesnt_exist():
    _, chunk_size, overlap = defaults()
    payload = get_payload('get_webpage_chunks', url_doesnt_exist(), chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL does not exist'


def test_get_webpage_bad_xpath():
    url = working_url()
    xpaths = ['this_is_not_an_xpath']
    payload = get_payload('get_webpage_xpaths', url, xpaths)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == xpaths[0] + ' is not an xpath'


def test_get_webpage_xpaths():
    url = working_url()
    xpaths = [
        '/html/body/div[3]/div[1]/div/div/section/h1',
        '/html/body/div[5]'
    ]
    xpath_string = 'The Python Software Foundation is a non-profit corporation.'
    payload = get_payload('get_webpage_xpaths', url, xpaths)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'success'
    assert response_json['result']['response'][0] == 'History and License'
    assert xpath_string in response_json['result']['response'][1]
