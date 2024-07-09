storage_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {"inputs": {"initial_storage": str}, "output": str},
                "get_storage": {"output": str},
                "update_storage": {"inputs": {"new_storage": str}, "output": str},
            },
        },
        "status": str,
    },
}
