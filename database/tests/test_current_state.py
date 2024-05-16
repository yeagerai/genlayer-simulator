import re
import json
from time import sleep

from rpc.utils import create_new_address
from database.init_db import clear_db_tables
from database.functions import DatabaseFunctions


def _clear_tables():
    clear_db_tables(None, ["current_state"])

def _random_current_state_data():
    return _current_state_data(create_new_address())

def _current_state_data(id:str="0x123"):
    return {
        "id": id,
        "data": json.dumps({"key": "value"}),
    }


def test_insert_current_state():
    _clear_tables()
    random_current_state_data = _random_current_state_data()
    with DatabaseFunctions() as dbf:
        current_state = dbf.insert_current_state(**random_current_state_data)
        dbf.close()

    assert current_state["id"] == random_current_state_data["id"]
    assert current_state["data"] == random_current_state_data["data"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", current_state["updated_at"])

def test_get_current_state():
    _clear_tables()
    random_current_state_data = _random_current_state_data()
    with DatabaseFunctions() as dbf:
        insert_current_state_result = dbf.insert_current_state(**random_current_state_data)
        current_state = dbf.get_current_state(insert_current_state_result["id"])
        dbf.close()

    assert current_state["id"] == random_current_state_data["id"]
    assert current_state["data"] == random_current_state_data["data"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", current_state["updated_at"])

def test_update_current_state():
    _clear_tables()
    new_data = {"key_2": "value_2"}
    random_current_state_data = _random_current_state_data()
    with DatabaseFunctions() as dbf:
        insert_current_state_result = dbf.insert_current_state(**random_current_state_data)
        dbf.connection.commit()
        sleep(1)
        current_state = dbf.update_current_state(insert_current_state_result["id"], data=json.dumps(new_data))
        dbf.close()

    current_state_data = json.loads(current_state["data"])
    assert current_state["id"] == random_current_state_data["id"]
    assert current_state_data == new_data
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", current_state["updated_at"])
    assert current_state["updated_at"] != insert_current_state_result["updated_at"]
