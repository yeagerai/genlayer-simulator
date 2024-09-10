call_contract_function_response = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "consensus_data": {
                "final": bool,
                "leader_receipt": {
                    "args": list,
                    "class_name": str,
                    "contract_state": str,
                    "eq_outputs": {"leader": dict},
                    "error": str | None,
                    "execution_result": str,
                    "gas_used": int,
                    "method": str,
                    "mode": str,
                    "node_config": {
                        "config": dict,
                        "model": str,
                        "provider": str,
                        "stake": int,
                    },
                    "vote": str,
                },
                "validators": list,
                "votes": dict,
            },
            "created_at": str,
            "data": {
                "function_args": str,  # TODO: can we make this a list?
                "function_name": str,
            },
            "from_address": str,
            "id": int,
            "status": str,
            "to_address": str,
            "type": int,
            "value": float,
        },
        "message": str,
        "status": str,
    },
}
