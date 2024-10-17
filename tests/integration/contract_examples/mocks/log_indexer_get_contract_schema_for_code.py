log_indexer_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "abi": [
            {"inputs": [], "type": "constructor"},
            {
                "inputs": [
                    {"name": "log", "type": "string"},
                    {"name": "log_id", "type": "int"},
                ],
                "name": "add_log",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [{"name": "text", "type": "string"}],
                "name": "get_closest_vector",
                "outputs": [{"name": "", "type": "any"}],
                "type": "function",
            },
            {
                "inputs": [{"name": "id", "type": "int"}],
                "name": "get_vector_metadata",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [{"name": "id", "type": "int"}],
                "name": "remove_log",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [
                    {"name": "id", "type": "int"},
                    {"name": "log", "type": "string"},
                    {"name": "log_id", "type": "int"},
                ],
                "name": "update_log",
                "outputs": [],
                "type": "function",
            },
        ],
        "class": "LogIndexer",
    },
}
