# consensus/services/genvm_service.py

import requests

from node.errors import GenVMRPCErrorResponse
from node.clients.rpc_client import RPCClient


class GenVMService:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client

    def deploy_contract(
        self,
        from_address: str,
        contract_code: str,
        constructor_args: str,
        class_name: str,
        leader_config: dict,
    ) -> dict:
        params = [
            from_address,
            contract_code,
            constructor_args,
            class_name,
            leader_config,
        ]
        result = self.rpc_client.call("deploy_contract", params)
        return result["data"]

    def get_contract_schema(self, contract_code: str) -> dict:
        params = [contract_code]
        return self.rpc_client.call("get_icontract_schema", params)

    def get_contract_state(
        self,
        contract_code: str,
        contract_state: dict,
        method_name: str,
        method_args: list,
    ) -> dict:
        params = [contract_code, contract_state, method_name, method_args]
        return self.rpc_client.call("get_contract_data", params)
