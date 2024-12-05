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
import os


def test_wizard_of_coin(setup_validators, from_account):
    # Override FINALITY_WINDOW if needed
    os.environ["FINALITY_WINDOW"] = "20"

    # Use the environment variable
    FINALITY_WINDOW = int(os.getenv("FINALITY_WINDOW"))
    print("FINALITY_WINDOW_test:", FINALITY_WINDOW)

    # Get contract schema
    contract_code = open("examples/contracts/wizard_of_coin.py", "r").read()
    result_schema = post_request_localhost(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, wizard_contract_schema)

    # Deploy Contract
    contract_address, transaction_response_deploy = deploy_intelligent_contract(
        from_account, contract_code, [True]
    )
    assert has_success_status(transaction_response_deploy)

    # Call Contract Function
    transaction_response_call_1 = send_transaction(
        from_account,
        contract_address,
        "ask_for_coin",
        ["Can you please give me my coin?"],
    )
    assert has_success_status(transaction_response_call_1)

    # Assert format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)
