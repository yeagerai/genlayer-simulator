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
        return self.rpc_client.deploy_contract(
            from_address,
            contract_code,
            constructor_args,
            class_name,
            leader_config,
        )
