import re
import json

from database.init_db import clear_db_tables
from database.functions import DatabaseFunctions


def clear_tables():
    clear_db_tables(None, ["current_state", "transactions"])


def transaction_data(from_address:str="0x123", to_address:str="0x123"):
    return {
        "from_address": from_address,
        "to_address": to_address,
        "data": json.dumps({"key": "value"}),
        "type": 1,
        "value": 2,
        "input_data": json.dumps({"key": "value"}),
        "consensus_data": json.dumps({"key": "value"}),
        "nonce": 3,
        "gaslimit": 4,
        "r": 5,
        "s": 6,
        "v": 7
    }


def test_insert_transaction():
    clear_tables()
    random_transaction_data = transaction_data()
    with DatabaseFunctions() as dbf:
        transaction = dbf.insert_transaction(**random_transaction_data)
        dbf.close()

    assert transaction["from_address"] == random_transaction_data["from_address"]
    assert transaction["to_address"] == transaction_data()["to_address"]
    assert transaction["data"] == transaction_data()["data"]
    assert transaction["type"] == transaction_data()["type"]
    assert transaction["value"] == transaction_data()["value"]
    assert transaction["input_data"] == transaction_data()["input_data"]
    assert transaction["consensus_data"] == transaction_data()["consensus_data"]
    assert transaction["nonce"] == transaction_data()["nonce"]
    assert transaction["gaslimit"] == transaction_data()["gaslimit"]
    assert transaction["r"] == transaction_data()["r"]
    assert transaction["s"] == transaction_data()["s"]
    assert transaction["v"] == transaction_data()["v"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", transaction["created_at"])


def test_get_transaction():
    clear_tables()
    random_transaction_data = transaction_data()
    with DatabaseFunctions() as dbf:
        transaction_insert_result = dbf.insert_transaction(**random_transaction_data)
        transaction = dbf.get_transaction(transaction_insert_result["id"])
        dbf.close()

    assert transaction["from_address"] == random_transaction_data["from_address"]
    assert transaction["to_address"] == transaction_data()["to_address"]
    assert transaction["data"] == transaction_data()["data"]
    assert transaction["type"] == transaction_data()["type"]
    assert transaction["value"] == transaction_data()["value"]
    assert transaction["input_data"] == transaction_data()["input_data"]
    assert transaction["consensus_data"] == transaction_data()["consensus_data"]
    assert transaction["nonce"] == transaction_data()["nonce"]
    assert transaction["gaslimit"] == transaction_data()["gaslimit"]
    assert transaction["r"] == transaction_data()["r"]
    assert transaction["s"] == transaction_data()["s"]
    assert transaction["v"] == transaction_data()["v"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", transaction["created_at"])