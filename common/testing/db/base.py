import os
import json

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


def current_state_data(id:str="0x123"):
    return {
        "id": id,
        "data": json.dumps({"key": "value"})
    }


def setup_db_and_tables():
    create_db_if_it_doesnt_already_exists()
    create_tables_if_they_dont_already_exist(None)
    clear_db_tables(None, all_tables)