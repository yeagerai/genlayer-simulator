wizard_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {"inputs": {"have_coin": str}, "output": str},
                "ask_for_coin": {"inputs": {"request": str}, "output": str},
                "get_have_coin": {"output": str},
            },
        },
        "status": str,
    },
}
