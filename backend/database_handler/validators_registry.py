# consensus/domain/state.py

import json
from psycopg2.extras import Json
from backend.database_handler import models
from backend.database_handler.db_client import DBClient

from backend.errors.errors import ValidatorNotFound

from sqlalchemy.orm import Session


# the to_dict function lives in this module and not in models.py because it's on this layer of abstraction where we convert database objects to our custom data structures
def to_dict(validator: models.Validators) -> dict:
    return {
        "id": validator.id,
        "address": validator.address,
        "stake": validator.stake,
        "provider": validator.provider,
        "model": validator.model,
        "config": validator.config,
        "created_at": validator.created_at.isoformat(),
    }


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
            "config": validator_data["config"],
            "created_at": validator_data["created_at"].isoformat(),
        }

    def _get_validator_or_fail(self, validator_address: str):
        """Private method to check if an account exists, and raise an error if not."""

        with Session(self.db_client.engine) as session:
            validator_data = (
                session.query(models.Validators)
                .filter_by(address=validator_address)
                .first()
            )

        if not validator_data:
            raise ValidatorNotFound(validator_address)
        return to_dict(validator_data)

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
            "config": Json(config),
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
        self._get_validator_or_fail(validator_address)

        update_condition = f"address = '{validator_address}'"
        validator = {
            "stake": stake,
            "provider": provider,
            "model": model,
            "config": Json(config),
        }

        self.db_client.update(self.db_validators_table, validator, update_condition)
        return self._get_validator_or_fail(validator_address)

    def delete_validator(self, validator_address):
        self._get_validator_or_fail(validator_address)
        delete_condition = f"address = '{validator_address}'"
        self.db_client.remove(self.db_validators_table, delete_condition)

    def delete_all_validators(self):
        self.db_client.remove_all(self.db_validators_table)
