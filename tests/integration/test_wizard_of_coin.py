# tests/e2e/test_wizard_of_coin.py

from tests.common.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tests.integration.mocks.wizard_get_contract_schema_for_code import (
    wizard_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)


def test_wizard_of_coin():
    print("test_wizard_of_coin")
    # Validators
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"], None, "gpt-4o-mini")
    ).json()
    assert has_success_status(result)

    # Account
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address = result["result"]["data"]["account_address"]

    # Get contract schema
    contract_code = open("examples/contracts/wizard_of_coin.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, wizard_contract_schema)

    # Deploy Contract
    data = [
        from_address,  # from_account
        "WizardOfCoin",  # class_name
        contract_code,  # contract_code
        '{"have_coin": true}',  # initial_state
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # Call Contract Function
    function = "ask_for_coin"
    args = ["Can you please give me my coin?"]
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function", from_address, contract_address, function, args
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
