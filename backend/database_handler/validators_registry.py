# consensus/domain/state.py

import json

from backend.database_handler.db_client import DBClient

from backend.errors.errors import ValidatorNotFound


class ValidatorsRegistry:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client
        self.db_validators_table = "validators"

    def _parse_validator_data(self, validator_data: dict) -> dict:
        return {
            "id": validator_data["id"],
            "address": validator_data["address"],
            "stake": float(validator_data["stake"]),
            "provider": validator_data["provider"],
            "model": validator_data["model"],
            "config": json.loads(validator_data["config"]),
            "created_at": validator_data["created_at"].isoformat(),
        }

    def _get_validator_or_fail(self, validator_address: str):
        """Private method to check if an account exists, and raise an error if not."""
        condition = f"address = '{validator_address}'"
        result = self.db_client.get(self.db_validators_table, condition)

        validator_data = result[0] if result else None

        if not validator_data:
            raise ValidatorNotFound(validator_address)
        return self._parse_validator_data(validator_data)

    def count_validators(self):
        return self.db_client.count(self.db_validators_table)

    def get_all_validators(self) -> list:
        validators_data = self.db_client.get(self.db_validators_table)
        return [self._parse_validator_data(validator) for validator in validators_data]

    def get_validator(self, validator_address: str) -> dict:
        return self._get_validator_or_fail(validator_address)

    def create_validator(
        self,
        validator_address: str,
        stake: int,
        provider: str,
        model: str,
        config: json,
    ):
        new_validator = {
            "address": validator_address,
            "stake": stake,
            "provider": provider,
            "model": model,
            "config": json.dumps(config),
            "created_at": "CURRENT_TIMESTAMP",
        }
        self.db_client.insert(self.db_validators_table, new_validator)
        return self._get_validator_or_fail(validator_address)

    def update_validator(
        self,
        validator_address: str,
        stake: int,
        provider: str,
        model: str,
        config: json,
    ):
        validator = self._get_validator_or_fail(validator_address)

        update_condition = f"address = '{validator_address}'"
        validator = {
            "stake": stake,
            "provider": provider,
            "model": model,
            "config": json.dumps(config),
        }

        self.db_client.update(self.db_validators_table, validator, update_condition)
        return self._get_validator_or_fail(validator_address)

    def delete_validator(self, validator_address):
        self._get_validator_or_fail(validator_address)
        delete_condition = f"address = '{validator_address}'"
        self.db_client.remove(self.db_validators_table, delete_condition)

    def delete_all_validators(self):
        self.db_client.remove_all(self.db_validators_table)
