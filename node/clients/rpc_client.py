# consensus/clients/rpc_client.py

import requests
import uuid

from node.errors import GenVMRPCErrorResponse


class RPCClient:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.jsonrpc = "2.0"

    def call(self, method: str, params: list) -> dict:
        payload = {
            "jsonrpc": self.jsonrpc,
            "method": method,
            "params": params,
            "id": str(uuid.uuid4()),
        }
        response = requests.post(self.rpc_url + "/api", json=payload).json()

        if response["result"]["status"] == "error":
            raise GenVMRPCErrorResponse(response["result"]["data"])

        return response["result"]
