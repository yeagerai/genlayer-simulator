user_storage_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {"output": str},
                "get_complete_storage": {"output": str},
                "get_account_storage": {
                    "inputs": {"account_address": str},
                    "output": str,
                },
                "update_storage": {"inputs": {"new_storage": str}, "output": str},
            },
        },
        "status": str,
    },
}
