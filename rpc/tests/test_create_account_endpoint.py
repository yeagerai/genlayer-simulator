from common.testing.db.base import setup_db_and_tables
from database.init_db import drop_db_if_it_already_exists
from common.address import address_is_in_correct_format
from rpc.tests.base import (
    payload,
    post_request,
    get_all_rows_for_table
)

def num_rows_in_current_state_table() -> int:
    response = get_all_rows_for_table("current_state")
    print(response)
    return len(response)


def test_create_account_endpoint():
    setup_db_and_tables()

    post_request(payload("create_db"))
    post_request(payload("create_tables"))

    assert num_rows_in_current_state_table() == 0

    response_1 = post_request(payload("create_account")).json()
    assert response_1["result"]["status"] == "success"
    assert address_is_in_correct_format(response_1["result"]["data"]["address"])
    assert response_1["result"]["data"]["balance"] == 0

    # Make sure it's creating random addresses
    response_2 = post_request(payload("create_account")).json()
    response_1_address = response_1["result"]["data"]["address"]
    response_2_address = response_2["result"]["data"]["address"]
    assert response_1_address != response_2_address

    assert num_rows_in_current_state_table() == 2


def test_create_account_endpoint_database_does_not_exist():
    drop_db_if_it_already_exists()
    response = post_request(payload("create_account")).json()
    assert response["result"]["status"] == "error"
    assert 'database "genlayer_state" does not exist' in response["result"]["message"]
    assert "traceback" in response["result"]["data"]