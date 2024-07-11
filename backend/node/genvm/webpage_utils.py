import os
import requests
import re


def get_webpage_content(url: str) -> str:

    payload = {
        "jsonrpc": "2.0",
        "method": "get_webpage",
        "params": [url],
        "id": 2,
    }

    result = requests.post(webrequest_url() + "/api", json=payload).json()

    if result["result"]["status"] == "error":
        raise Exception(result["result"])

    return result["result"]


def webrequest_url():
    return (
        os.environ["WEBREQUESTPROTOCOL"]
        + "://"
        + os.environ["WEBREQUESTHOST"]
        + ":"
        + os.environ["WEBREQUESTPORT"]
    )
