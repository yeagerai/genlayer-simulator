# consensus/services/state_db_service.py

import json

from database.db_client import DBClient


class ValidatorsDBService:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client
        self.db_state_table = "validators"

    def parse_validator_result(self, validator_result: list) -> dict:
        return {
            "id": validator_result[0],
            "address": validator_result[1],
            "stake": float(validator_result[2]),
            "provider": validator_result[3],
            "model": validator_result[4],
            "config": validator_result[5],
            "updated_at": validator_result[6].strftime("%m/%d/%Y, %H:%M:%S"),
        }

    def count_validators(self) -> int:
        return self.db_client.count(self.db_state_table)

    def get_all_validators(self) -> list:
        result = self.db_client.get(self.db_state_table)
        validators = []
        for validator in result:
            validators.append(self.parse_validator_result(validator))
        return validators

    def get_validator_by_address(self, validator_address: str) -> dict:
        condition = f"address = '{validator_address}'"
        result = self.db_client.get(self.db_state_table, condition)
        if result:
            return self.parse_validator_result(result[0])
        return None

    def create_validator(self, validator_data: dict) -> dict:
        validator = {
            "address": validator_data["address"],
            "stake": validator_data["stake"],
            "provider": validator_data["provider"],
            "model": validator_data["model"],
            "config": validator_data["config"],
            "created_at": "CURRENT_TIMESTAMP",
        }
        self.db_client.insert(self.db_state_table, validator)
        return validator

    def update_validator(self, validator_data: dict) -> None:
        update_condition = f"address = '{validator_data['address']}'"
        validator = {
            "stake": validator_data["stake"],
            "provider": validator_data["provider"],
            "model": validator_data["model"],
            "config": validator_data["config"],
            "created_at": "CURRENT_TIMESTAMP",
        }
        self.db_client.update(self.db_state_table, validator, update_condition)
        return validator

    def delete_validator(self, validator_address: str) -> None:
        delete_condition = f"address = '{validator_address}'"
        self.db_client.remove(self.db_state_table, delete_condition)

    def delete_all_validators(self) -> None:
        self.db_client.remove_all(self.db_state_table)
