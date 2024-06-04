from common.testing.requests import payload, post_request_localhost
from common.testing.structure import execute_icontract_function_response_structure
from common.testing.response import (
    assert_dict_struct,
    has_success_status,
)

'''
def test_wizard_of_coin():

    # DB
    result = post_request_localhost(payload("create_db")).json()
    assert has_success_status(result)
    result = post_request_localhost(payload("create_tables")).json()
    assert has_success_status(result)

    # Validators
    result = post_request_localhost(
        payload(
            "create_random_validators",
            10,
            8.0,
            12.0
        )
    ).json()
    assert has_success_status(result)

    # Account
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "address" in result["result"]["data"]
    from_address = result["result"]["data"]["address"]
    result = post_request_localhost(payload("fund_account", from_address, 10.0)).json()
    assert has_success_status(result)

    # Deploy Contract
    contract_code = open("examples/contracts/wizard_of_coin.py", "r").read()
    data = [
        from_address,            # from_account
        "WizardOfCoin",          # class_name
        contract_code,           # contract_code
        '{"have_coin": "True"}'  # initial_state
    ]
    result = post_request_localhost(payload("deploy_intelligent_contract", *data))
    try:
        result_json = result.json()
        assert True
    except Exception:
        print(result.text)
        assert False
    assert has_success_status(result_json)
    contract_address = result_json["result"]["data"]["contract_id"]

    # Execute Contract
    function = "WizardOfCoin.ask_for_coin"
    args = ["Can you please give me my coin?"]
    result = post_request_localhost(
        payload(
            "call_contract_function",
            from_address,
            contract_address,
            function,
            args
        )
    )
    try:
        result_json = result.json()
        assert True
    except Exception:
        print(result.text)
        assert False

    # Assert format
    print(result_json)
    assert_dict_struct(result_json, execute_icontract_function_response_structure)
'''