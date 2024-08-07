# consensus/domain/state.py

from backend.database_handler import models

from backend.errors.errors import ValidatorNotFound

from sqlalchemy.orm import Session
from sqlalchemy import Engine


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
    def __init__(self, engine: Engine):
        self.engine = engine
        self.db_validators_table = "validators"

    def _get_validator_or_fail(self, validator_address: str):
        """Private method to check if an account exists, and raise an error if not."""

        with Session(self.engine) as session:
            validator_data = (
                session.query(models.Validators)
                .filter(models.Validators.address == validator_address)
                .one_or_none()
            )

        if validator_data is None:
            raise ValidatorNotFound(validator_address)
        return to_dict(validator_data)

    def count_validators(self):
        with Session(self.engine) as session:
            return session.query(models.Validators).count()

    def get_all_validators(self) -> list:
        with Session(self.engine) as session:
            validators_data = session.query(models.Validators).all()
            return [to_dict(validator) for validator in validators_data]

    def get_validator(self, validator_address: str) -> dict:
        return self._get_validator_or_fail(validator_address)

    def create_validator(
        self,
        validator_address: str,
        stake: int,
        provider: str,
        model: str,
        config: dict,
    ):
        new_validator = models.Validators(
            address=validator_address,
            stake=stake,
            provider=provider,
            model=model,
            config=config,
        )

        with Session(self.engine) as session:
            session.add(new_validator)
            session.commit()

        return self._get_validator_or_fail(validator_address)

    def update_validator(
        self,
        validator_address: str,
        stake: int,
        provider: str,
        model: str,
        config: dict,
    ):
        self._get_validator_or_fail(validator_address)

        with Session(self.engine) as session:
            validator = (
                session.query(models.Validators)
                .filter(models.Validators.address == validator_address)
                .one()
            )

            validator.stake = stake
            validator.provider = provider
            validator.model = model
            validator.config = config

            session.commit()

            return to_dict(validator)

    def delete_validator(self, validator_address):
        self._get_validator_or_fail(validator_address)

        with Session(self.engine) as session:
            session.query(models.Validators).filter(
                models.Validators.address == validator_address
            ).delete()
            session.commit()

    def delete_all_validators(self):
        with Session(self.engine) as session:
            session.query(models.Validators).delete()
            session.commit()
