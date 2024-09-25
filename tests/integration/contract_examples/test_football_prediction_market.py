# tests/e2e/test_storage.py

from tests.common.request import (
    deploy_intelligent_contract,
    send_transaction,
    payload,
    post_request_localhost,
)
from tests.integration.contract_examples.mocks.football_prediction_market_get_contract_schema_for_code import (
    football_prediction_market_contract_schema,
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


def test_football_prediction_market(setup_validators, from_account):
    # Get contract schema
    contract_code = open("examples/contracts/football_prediction_market.py", "r").read()
    result_schema = post_request_localhost(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, football_prediction_market_contract_schema)

    # Deploy Contract
    _, transaction_response_deploy = deploy_intelligent_contract(
        from_account,
        contract_code,
        f'{{"game_date": "2024-06-26", "team1": "Georgia", "team2": "Portugal"}}',
    )
    assert has_success_status(transaction_response_deploy)
    contract_address = transaction_response_deploy["data"]["contract_address"]

    ########################################
    ############# RESOLVE match ############
    ########################################
    _, transaction_response_call_1 = send_transaction(
        from_account,
        contract_address,
        "resolve",
        [],
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)
