# consensus/clients/rpc_client.py

import requests

from consensus.errors import GenVMRPCErrorResponse


class RPCClient:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.jsonrpc = "2.0"

    def deploy_contract(
        self,
        from_address: str,
        contract_code: str,
        constructor_args: str,
        class_name: str,
        leader_config: dict,
    ) -> dict:
        payload = {
            "jsonrpc": self.jsonrpc,
            "method": "deploy_contract",
            "params": [
                from_address,
                contract_code,
                constructor_args,
                class_name,
                leader_config,
            ],
            "id": 3,
        }
        response = requests.post(self.rpc_url + "/api", json=payload).json()

        if response["result"]["status"] == "error":
            raise GenVMRPCErrorResponse(response["result"]["data"])

        return response["result"]["data"]
