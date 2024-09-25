import os

from tests.common.request import (
    call_contract_method,
    deploy_intelligent_contract,
)
from tests.common.response import has_success_status


def test_async_init(setup_validators, from_account):

    current_directory = os.path.dirname(os.path.abspath(__file__))
    contract_file = os.path.join(current_directory, "async_init.py")

    contract_code = open(contract_file, "r").read()

    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(
            from_account,
            contract_code,
            "{}",
        )
    )
    assert has_success_status(transaction_response_deploy)

    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    contract_state = call_contract_method(
        contract_address, from_account, "get_result", []
    )
    assert has_success_status(contract_state)

    result = contract_state["result"]["data"]

    assert isinstance(result, str)
    assert result != ""
