football_prediction_market_contract_schema = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "class": str,
            "methods": {
                "__init__": {
                    "inputs": {"game_date": str, "team1": str, "team2": str},
                    "output": str,
                },
                "resolve": {"output": str},
            },
            "variables": {},
        },
        "message": str,
        "status": str,
    },
}
