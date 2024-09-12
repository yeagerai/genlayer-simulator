# tests/e2e/test_wizard_of_coin.py

from tests.common.request import (
    deploy_intelligent_contract,
    send_transaction,
    payload,
    post_request_localhost,
)
from tests.integration.contract_examples.mocks.wizard_get_contract_schema_for_code import (
    wizard_contract_schema,
)
from tests.integration.contract_examples.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    assert_dict_exact,
    has_success_status,
)

from tests.common.accounts import create_new_account


def test_wizard_of_coin():
    print("test_wizard_of_coin")
    # Validators
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"], None, "gpt-4o-mini")
    ).json()
    assert has_success_status(result)

    # Account Setup
    from_account = create_new_account()

    # Get contract schema
    contract_code = open("examples/contracts/wizard_of_coin.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, wizard_contract_schema)

    # Deploy Contract
    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(
            from_account, contract_code, f'{{"have_coin": true}}'
        )
    )
    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # Call Contract Function
    _, transaction_response_call_1 = send_transaction(
        from_account,
        contract_address,
        "ask_for_coin",
        ["Can you please give me my coin?"],
    )
    assert has_success_status(transaction_response_call_1)

    # Assert format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
