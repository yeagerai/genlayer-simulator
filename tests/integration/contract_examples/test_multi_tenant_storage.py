import json
import os

from tests.common.accounts import create_new_account
from tests.common.request import (
    call_contract_method,
    deploy_intelligent_contract,
    send_transaction,
)
from tests.common.response import has_success_status


def test_multi_tenant_storage(setup_validators):
    """
    This test verifies the functionality of a multi-read ERC20 contract. It deploys two separate ERC20 token contracts
    (referred to as 'doge' and 'shiba') and a multi-read ERC20 contract. The test aims to:

    1. Deploy two different ERC20 token contracts with a total supply of 1000 tokens each.
    2. Deploy a multi-read ERC20 contract that can interact with multiple ERC20 tokens.
    3. Test the ability of the multi-read contract to update and retrieve token balances for multiple ERC20 tokens
       and multiple accounts simultaneously.
    4. Ensure the multi-read contract correctly maintains and reports balances for different account-token combinations.

    This test demonstrates the integration contract to contract reads
    """
    main_account = create_new_account()
    user_account_a = create_new_account()
    user_account_b = create_new_account()

    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Storage Contracts
    contract_code = open("examples/contracts/storage.py", "r").read()

    ## Deploy first Storage Contract
    first_storage_contract_address, transaction_response_deploy = (
        deploy_intelligent_contract(
            main_account,
            contract_code,
            json.dumps({"initial_storage": "initial_storage_a"}),
        )
    )
    assert has_success_status(transaction_response_deploy)

    ## Deploy second Storage Contract

    second_storage_contract_address, transaction_response_deploy = (
        deploy_intelligent_contract(
            main_account,
            contract_code,
            json.dumps({"initial_storage": "initial_storage_b"}),
        )
    )
    assert has_success_status(transaction_response_deploy)

    # Deploy Multi Tenant Storage Contract
    contract_file = os.path.join(current_directory, "multi_tenant_storage.py")
    contract_code = open(contract_file, "r").read()

    multi_tenant_storage_address, transaction_response_deploy = (
        deploy_intelligent_contract(
            main_account,
            contract_code,
            json.dumps(
                {
                    "storage_contracts": [
                        first_storage_contract_address,
                        second_storage_contract_address,
                    ]
                }
            ),
        )
    )
    assert has_success_status(transaction_response_deploy)

    # update storage for first contract
    transaction_response_call = send_transaction(
        user_account_a,
        multi_tenant_storage_address,
        "update_storage",
        ["user_a_storage"],
    )

    assert has_success_status(transaction_response_call)

    # update storage for second contract
    transaction_response_call = send_transaction(
        user_account_b,
        multi_tenant_storage_address,
        "update_storage",
        ["user_b_storage"],
    )

    assert has_success_status(transaction_response_call)

    # TODO: we might need to wait for the transactions to be processed before getting the storages
    # get all storages
    storages = call_contract_method(
        main_account,
        multi_tenant_storage_address,
        "get_all_storages",
        [],
    )

    assert storages == {
        first_storage_contract_address: "user_a_storage",
        second_storage_contract_address: "user_b_storage",
    }
