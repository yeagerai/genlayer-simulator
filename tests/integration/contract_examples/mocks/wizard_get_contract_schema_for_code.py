wizard_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "abi": [
            {
                "inputs": [{"name": "have_coin", "type": "bool"}],
                "type": "constructor",
            },
            {
                "inputs": [{"name": "request", "type": "string"}],
                "name": "ask_for_coin",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [],
                "name": "get_have_coin",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function",
            },
        ],
        "class": "WizardOfCoin",
    },
}
