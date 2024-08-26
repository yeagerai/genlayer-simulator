llm_erc20_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "data": {
            "abi": [
                {
                    "inputs": [{"name": "total_supply", "type": "uint256"}],
                    "type": "constructor",
                },
                {
                    "inputs": [{"name": "address", "type": "string"}],
                    "name": "get_balance_of",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function",
                },
                {
                    "inputs": [],
                    "name": "get_balances",
                    "outputs": [{"name": "", "type": ", in"}],
                    "type": "function",
                },
                {
                    "inputs": [
                        {"name": "amount", "type": "uint256"},
                        {"name": "to_address", "type": "string"},
                    ],
                    "name": "transfer",
                    "outputs": [],
                    "type": "function",
                },
            ],
            "class": "LlmErc20",
        },
        "exception": None,
        "message": "Endpoint get_contract_schema_for_code successfully executed",
        "status": "success",
    },
}
