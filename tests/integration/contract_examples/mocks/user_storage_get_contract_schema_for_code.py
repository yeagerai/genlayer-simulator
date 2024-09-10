user_storage_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "data": {
            "abi": [
                {"inputs": [], "type": "constructor"},
                {
                    "inputs": [{"name": "account_address", "type": "string"}],
                    "name": "get_account_storage",
                    "outputs": [{"name": "", "type": "string"}],
                    "type": "function",
                },
                {
                    "inputs": [],
                    "name": "get_complete_storage",
                    "outputs": [{"name": "", "type": "bytes"}],
                    "type": "function",
                },
                {
                    "inputs": [{"name": "new_storage", "type": "string"}],
                    "name": "update_storage",
                    "outputs": [],
                    "type": "function",
                },
            ],
            "class": "UserStorage",
        },
        "exception": None,
        "message": "Endpoint get_contract_schema_for_code successfully executed",
        "status": "success",
    },
}
