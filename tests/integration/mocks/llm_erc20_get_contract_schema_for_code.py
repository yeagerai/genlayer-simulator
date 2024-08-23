llm_erc20_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {"inputs": {"total_supply": int}},
                "get_balance_of": {"inputs": {"address": str}, "output": int},
                "get_balances": {"output": dict},
                "transfer": {
                    "inputs": {"amount": int, "to_address": str},
                    "output": str,
                },
            },
        },
        "message": str,
        "status": str,
    },
}
