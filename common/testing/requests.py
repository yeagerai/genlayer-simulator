import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()


def payload(function_name:str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(
    payload:dict,
    protocol:str=os.environ['RPCPROTOCOL'],
    host:str=os.environ['RPCHOST'],
    port:str=os.environ['RPCPORT']
):
    return requests.post(
        protocol+"://"+host+":"+port+"/api",
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

def post_request_localhost(payload:dict):
    return post_request(payload, "http", "localhost")