import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()


def not_url() -> str:
    return '<this_is_not_a_URL>'

def url_doesnt_exist() -> str:
    return 'http://www.urlthatdoesntexist.com/'

def working_url() -> str:
    return 'https://docs.python.org/3/license.html'


def get_payload(function_name:str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(payload:dict):
    return requests.post(
        "http://localhost:"+os.environ['WEBREQUESTPORT']+"/api",
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )