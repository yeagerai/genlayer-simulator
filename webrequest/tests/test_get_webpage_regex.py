import json

from tests.base import not_url, url_doesnt_exist, working_url, get_payload, post_request


def defaults():
    url = "https://docs.python.org/3/license.html"
    regex = r'<section id="history-and-license">.*?\<\/a\>'
    return url, regex


def test_get_webpage_regex_bad_url():
    _, regex = defaults()
    payload = get_payload("get_webpage_regex", not_url(), regex)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json["result"]["status"] == "error"
    assert response_json["result"]["response"] == "URL not in correct format"


def test_get_webpage_regex_url_doesnt_exist():
    _, regex = defaults()
    payload = get_payload("get_webpage_regex", url_doesnt_exist(), regex)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json["result"]["status"] == "error"
    assert response_json["result"]["response"] == "URL does not exist"


def test_get_webpage_regex_bad_regex():
    url, _ = defaults()
    regex = r"this-regex-does-not-exist"
    payload = get_payload("get_webpage_regex", url, regex)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json["result"]["status"] == "error"
    assert "No matches were found" in response_json["result"]["response"]


def test_get_webpage_regex():
    url, regex = defaults()
    payload = get_payload("get_webpage_regex", url, regex)
    response = post_request(payload)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json["result"]["status"] == "success"
    assert response_json["result"]["response"][0] == "History and License"
