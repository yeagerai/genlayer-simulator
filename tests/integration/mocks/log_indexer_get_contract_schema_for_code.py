log_indexer_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {"inputs": {}, "output": str},
                "add_log": {"inputs": {"log": str, "log_id": int}, "output": str},
                "get_closest_vector": {"inputs": {"text": str}, "output": dict},
                "get_vector_metadata": {"inputs": {"id": int}, "output": str},
                "remove_log": {"inputs": {"id": int}, "output": str},
                "update_log": {
                    "inputs": {"id": int, "log": str, "log_id": int},
                    "output": str,
                },
            },
        },
        "message": str,
        "status": str,
    },
}
