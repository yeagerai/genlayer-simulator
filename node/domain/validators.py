# consensus/domain/state.py

import json

from node.services.validators_db_service import ValidatorsDBService
from node.errors import ValidatorNotFound


class Validators:
    def __init__(
        self,
        validators_db_service: ValidatorsDBService,
    ):
        self.validators_db_service = validators_db_service

    def _get_validator_or_fail(self, validator_address: str):
        """Private method to check if an account exists, and raise an error if not."""
        validator_data = self.validators_db_service.get_validator_by_address(
            validator_address
        )
        if not validator_data:
            raise ValidatorNotFound(validator_address)
        return validator_data

    def count_validators(self):
        return self.validators_db_service.count_validators()

    def get_all_validators(self):
        return self.validators_db_service.get_all_validators()

    def get_validator(self, validator_address):
        return self.validators_db_service.get_validator_by_address(validator_address)

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
            "config": config,
        }
        return self.validators_db_service.create_validator(new_validator)

    def update_validator(
        self,
        validator_address: str,
        stake: int,
        provider: str,
        model: str,
        config: json,
    ):
        validator = self._get_validator_or_fail(validator_address)

        validator["stake"] = stake
        validator["provider"] = provider
        validator["model"] = model
        validator["config"] = config

        return self.validators_db_service.update_validator(validator)

    def delete_validator(self, validator_address):
        self._get_validator_or_fail(validator_address)
        self.validators_db_service.delete_validator(validator_address)

    def delete_all_validators(self):
        self.validators_db_service.delete_all_validators()
