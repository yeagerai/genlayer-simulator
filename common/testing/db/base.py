import os
import json

from database.functions import DatabaseFunctions
from database.init_db import (
    create_db_if_it_doesnt_already_exists,
    create_tables_if_they_dont_already_exist,
    clear_db_tables
)

from dotenv import load_dotenv
load_dotenv()

db_name = os.environ['DBNAME']

all_tables = ["transactions", "transactions_audit", "current_state", "validators"]


def transaction_data(from_address:str="0x123", to_address:str="0x123"):
    return {
        "from_address": from_address,
        "to_address": to_address,
        "data": json.dumps({"key": "value"}),
        "input_data": json.dumps({"key": "value"}),
        "consensus_data": json.dumps({"key": "value"}),
        "nonce": 3,
        "value": 2,
        "type": 1,
        "status": "pending",
        "gaslimit": 4,
        "r": 5,
        "s": 6,
        "v": 7
    }


def assert_funds_transfer_data_in_db(transaction:list, address:str, data:dict, balance:float):
    assert transaction[1] == None
    assert transaction[2] == address
    assert transaction[3] == None
    assert transaction[4] == data
    assert transaction[5] == None
    assert transaction[6] == None
    assert transaction[7] == balance
    assert transaction[8] == 0
    assert transaction[9] == "pending"
    assert transaction[10] == None
    # Datetime stamp
    #assert transaction[11] == None
    assert transaction[12] == None
    assert transaction[13] == None
    assert transaction[14] == None


def current_state_data(id:str="0x123"):
    return {
        "id": id,
        "data": json.dumps({"key": "value"})
    }


def get_all_rows_for_table(table:str):
    with DatabaseFunctions() as db:
        db.cursor.execute(f"SELECT * FROM {table}")
        db.connection.commit()
        transactions = db.cursor.fetchall()
    return transactions


def assert_these_tables_are_empty(tables: list):
    for table in tables:
        assert get_all_rows_for_table(table) == []


def setup_db_and_tables():
    create_db_if_it_doesnt_already_exists()
    create_tables_if_they_dont_already_exist(None)
    clear_db_tables(None, all_tables)