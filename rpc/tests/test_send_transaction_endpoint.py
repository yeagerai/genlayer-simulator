import json

from database.functions import DatabaseFunctions
from common.testing.db.base import (
    setup_db_and_tables,
    get_all_rows_for_table,
    assert_these_tables_are_empty
)
from common.address import create_new_address
from common.testing.response.base import (
    has_error_status,
    has_success_status,
    has_message,
    has_data,
    message_is,
    data_is
)
from rpc.tests.base import payload, post_request

balanace = 10.0
amount = 2.0


def test_send_tansaction_endpoint_from_address_in_wrong_format():
    setup_db_and_tables()

    to_account = create_new_address()

    assert_these_tables_are_empty(["transactions", "current_state"])

    response = post_request(payload("send_transaction", "0x123", to_account, amount)).json()

    assert_these_tables_are_empty(["transactions", "current_state"])

    assert has_error_status(response)
    assert has_message(response)
    assert message_is(response, "from_account not in ethereum address format")


def test_send_tansaction_endpoint_to_address_in_wrong_format():
    setup_db_and_tables()

    from_account = create_new_address()

    assert_these_tables_are_empty(["transactions", "current_state"])

    response = post_request(payload("send_transaction", from_account, "0x123", amount)).json()

    assert_these_tables_are_empty(["transactions", "current_state"])

    assert has_error_status(response)
    assert has_message(response)
    assert message_is(response, "to_account not in ethereum address format")


def test_send_tansaction_endpoint_from_address_does_not_exist():
    setup_db_and_tables()

    from_account = create_new_address()
    to_account = create_new_address()

    assert_these_tables_are_empty(["transactions", "current_state"])

    response = post_request(payload("send_transaction", from_account, to_account, amount)).json()

    assert has_error_status(response)
    assert has_message(response)
    assert message_is(response, "from_account does not exist")


def test_send_tansaction_endpoint_to_address_does_not_exist():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    to_account = create_new_address()

    result_create_account = post_request(payload("create_account")).json()
    from_account = result_create_account["result"]["data"]["address"]
    post_request(payload("fund_account", from_account, balanace))
    response = post_request(payload("send_transaction", from_account, to_account, amount)).json()

    assert has_error_status(response)
    assert has_message(response)
    assert message_is(response, "to_account does not exist")


def test_send_tansaction_endpoint_insufficient_funds():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result_create_from_account = post_request(payload("create_account")).json()
    from_account = result_create_from_account["result"]["data"]["address"]
    result_create_to_account = post_request(payload("create_account")).json()
    to_account = result_create_to_account["result"]["data"]["address"]

    assert len(get_all_rows_for_table("current_state")) == 2

    response = post_request(payload("send_transaction", from_account, to_account, amount)).json()

    print(get_all_rows_for_table("current_state"))

    assert has_error_status(response)
    assert has_message(response)
    assert message_is(response, "insufficient funds")


def test_send_tansaction_endpoint():
    setup_db_and_tables()

    to_account = create_new_address()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result_create_from_account = post_request(payload("create_account")).json()
    from_account = result_create_from_account["result"]["data"]["address"]
    result_create_to_account = post_request(payload("create_account")).json()
    to_account = result_create_to_account["result"]["data"]["address"]

    post_request(payload("fund_account", from_account, balanace))

    response = post_request(payload("send_transaction", from_account, to_account, amount)).json()

    assert has_success_status(response)
    assert has_data(response)
    assert data_is(response, {"from_account": from_account, "to_account": to_account, "amount": amount})

    with DatabaseFunctions() as dbf:
        from_account_balance = json.loads(dbf.get_current_state(from_account)["data"])["balance"]
        to_account_balance = json.loads(dbf.get_current_state(to_account)["data"])["balance"]

    assert from_account_balance == balanace - amount
    assert to_account_balance == amount
