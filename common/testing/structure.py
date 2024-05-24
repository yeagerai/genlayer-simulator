execute_icontract_function_response_structure = {
    'id': int,
    'jsonrpc': str,
    'result': {
        'data': {
            'execution_output': {
                'consensus_data': str,
                'leader_data': {
                    'result': {
                        'args': list,
                        'class': str,
                        'contract_state': str,
                        'eq_outputs': {
                            'leader': {
                                '0': str
                            }
                        },
                        'gas_used': int,
                        'method': str,
                        'mode': str,
                        'node_config': {
                            'address': str,
                            'id': int,
                            'model': str,
                            'provider': str,
                            'stake': float,
                            'type': str,
                            'updated_at': str
                        }
                    },
                    'vote': str
                }
            }
        },
        'message': str,
        'status': str
    }
}
