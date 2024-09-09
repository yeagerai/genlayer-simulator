football_prediction_market_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "data": {
            "abi": [
                {
                    "inputs": [
                        {"name": "game_date", "type": "string"},
                        {"name": "team1", "type": "string"},
                        {"name": "team2", "type": "string"},
                    ],
                    "type": "constructor",
                },
                {"inputs": [], "name": "resolve", "outputs": [], "type": "function"},
            ],
            "class": "PredictionMarket",
        },
        "exception": None,
        "message": "Endpoint get_contract_schema_for_code successfully executed",
        "status": "success",
    },
}
