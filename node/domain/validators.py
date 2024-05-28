# consensus/domain/state.py

import json

from node.services.validators_db_service import ValidatorsDBService


class Validators:
    def __init__(
        self,
        validators_db_service: ValidatorsDBService,
    ):
        self.validators_db_service = validators_db_service

    def get_all_validators(self):
        return self.validators_db_service.get_all_validators()

    def get_validator(self, validator_address):
        return self.validators_db_service.get_validator_by_address(validator_address)

    def create_validator(self, validator):
        self.validators_db_service.create_validator(validator)

    def update_validator(self, validator):
        self.validators_db_service.update_validator(validator)

    def delete_validator(self, validator_address):
        self.validators_db_service.delete_validator(validator_address)

    def delete_all_validators(self, validator_address):
        self.validators_db_service.delete_all_validators(validator_address)
