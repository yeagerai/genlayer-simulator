import json
from math import floor

from tests.base import get_payload, post_request


def defaults():
    url = 'https://docs.python.org/3/license.html'
    chunck_size = 500
    overlap = 0.1
    return url, chunck_size, overlap


def test_get_webpage_bad_url():
    _, chunk_size, overlap = defaults()
    url = '<this_is_not_a_URL>'
    payload = get_payload('get_webpage_chunks', url, chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL not in correct format'


def test_get_webpage_url_doesnt_exist():
    _, chunk_size, overlap = defaults()
    url = 'http://www.urlthatdoesntexist.com/'
    payload = get_payload('get_webpage_chunks', url, chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'URL does not exist'


def test_get_webpage_overlap_too_small():
    url, chunk_size, _ = defaults()
    overlap = -0.2
    payload = get_payload('get_webpage_chunks', url, chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'Overlap should be between 0 and 0.4'


def test_get_webpage_overlap_too_large():
    url, chunk_size, _ = defaults()
    overlap = 0.6
    payload = get_payload('get_webpage_chunks', url, chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['result']['status'] == 'error'
    assert response_json['result']['response'] == 'Overlap should be between 0 and 0.4'


def test_get_webpage():
    url, chunk_size, overlap = defaults()
    payload = get_payload('get_webpage_chunks', url, chunk_size, overlap)
    response = post_request(payload)
    response_json = json.loads(response.text)
    chunks = response_json['result']['response']
    assert response.status_code == 200
    assert response_json['result']['status'] == 'success'
    # Just assert there are some chunks
    assert len(chunks) > 10
    # Check they are not the same
    for k, v in enumerate(chunks):
        if k > 0:
            assert v != chunks[k-1]
    # Check the top overlap of one is the same as the bottom overlap of two
    chunk_one = chunks[0]
    chunk_one_array = chunk_one.split(' ')
    chunk_two = chunks[1]
    chunk_two_array = chunk_two.split(' ')
    overlap_num = floor(chunk_size * overlap)
    top_of_chunk_one = ' '.join(chunk_one_array[-(overlap_num*2):])
    bottom_of_chunk_two = ' '.join(chunk_two_array[:(overlap_num*2)])
    assert top_of_chunk_one == bottom_of_chunk_two
