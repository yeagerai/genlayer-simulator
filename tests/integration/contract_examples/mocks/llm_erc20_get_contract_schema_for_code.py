llm_erc20_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "abi": [
            {
                "inputs": [{"name": "total_supply", "type": "int"}],
                "type": "constructor",
            },
            {
                "inputs": [{"name": "address", "type": "string"}],
                "name": "get_balance_of",
                "outputs": [{"name": "", "type": "int"}],
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
                    {"name": "amount", "type": "int"},
                    {"name": "to_address", "type": "string"},
                ],
                "name": "transfer",
                "outputs": [],
                "type": "function",
            },
        ],
        "class": "LlmErc20",
    },
}
