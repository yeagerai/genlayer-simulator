import re
import json

from common.address import create_new_address
from common.testing.db.base import setup_db_and_tables
from database.init_db import clear_db_tables
from database.functions import DatabaseFunctions


def random_validator_data():
    return validator_data(create_new_address())

def validator_data(address:str="0x123"):
    return {
        "address": address,
        "stake": 100,
        "provider": "provider",
        "model": "model",
        "config": json.dumps({"key": "value"}),
    }

def test_create_validator():
    setup_db_and_tables()
    with DatabaseFunctions() as dbf:
        validator = dbf.create_validator(**validator_data())
        dbf.close()

    assert validator["address"] == validator_data()["address"]
    assert validator["stake"] == validator_data()["stake"]
    assert validator["provider"] == validator_data()["provider"]
    assert validator["model"] == validator_data()["model"]
    assert json.dumps(validator["config"]) == validator_data()["config"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", validator["updated_at"])

def test_get__validator():
    setup_db_and_tables()
    with DatabaseFunctions() as dbf:
        new_validator = dbf.create_validator(**validator_data())
        validator = dbf.get_validator(new_validator['address'])
        dbf.close()

    assert validator["address"] == validator_data()["address"]
    assert validator["stake"] == validator_data()["stake"]
    assert validator["provider"] == validator_data()["provider"]
    assert validator["model"] == validator_data()["model"]
    assert json.dumps(validator["config"]) == validator_data()["config"]
    assert re.match(r"\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2}", validator["updated_at"])


def test_get_all_validators():
    setup_db_and_tables()
    with DatabaseFunctions() as dbf:
        dbf.create_validator(**random_validator_data())
        dbf.create_validator(**random_validator_data())
        dbf.create_validator(**random_validator_data())
        validators = dbf.all_validators()
        dbf.close()

    assert len(validators) == 3


def test_delete_validator():
    setup_db_and_tables()
    with DatabaseFunctions() as dbf:
        dbf.create_validator(**random_validator_data())
        dbf.create_validator(**random_validator_data())
        validator = dbf.create_validator(**random_validator_data())
        dbf.delete_validator(validator['address'])
        validators = dbf.all_validators()
        dbf.close()

    addresses = [v['address'] for v in validators]
    assert validator_data()['address'] not in addresses

def test_update_validator():
    setup_db_and_tables()
    with DatabaseFunctions() as dbf:
        validator = dbf.create_validator(**random_validator_data())
        updated_validator = dbf.update_validator(
            validator_address=validator['address'],
            stake=200,
            provider=validator['provider'],
            model=validator['model'],
            config=json.dumps(validator['config'])
        )
        dbf.close()

    assert updated_validator['stake'] == 200