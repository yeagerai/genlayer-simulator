log_indexer_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "data": {
            "abi": [
                {"inputs": [], "type": "constructor"},
                {
                    "inputs": [
                        {"name": "log", "type": "string"},
                        {"name": "log_id", "type": "uint256"},
                    ],
                    "name": "add_log",
                    "outputs": [],
                    "type": "function",
                },
                {
                    "inputs": [{"name": "text", "type": "string"}],
                    "name": "get_closest_vector",
                    "outputs": [{"name": "", "type": "bytes"}],
                    "type": "function",
                },
                {
                    "inputs": [{"name": "id", "type": "uint256"}],
                    "name": "get_vector_metadata",
                    "outputs": [],
                    "type": "function",
                },
                {
                    "inputs": [{"name": "id", "type": "uint256"}],
                    "name": "remove_log",
                    "outputs": [],
                    "type": "function",
                },
                {
                    "inputs": [
                        {"name": "id", "type": "uint256"},
                        {"name": "log", "type": "string"},
                        {"name": "log_id", "type": "uint256"},
                    ],
                    "name": "update_log",
                    "outputs": [],
                    "type": "function",
                },
            ],
            "class": "LogIndexer",
        },
        "exception": None,
        "message": "Endpoint get_contract_schema_for_code successfully executed",
        "status": "success",
    },
}
