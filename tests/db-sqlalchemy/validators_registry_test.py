from datetime import datetime
from typing import Iterable

import pytest
from sqlalchemy.orm import Session

from backend.database_handler.validators_registry import ValidatorsRegistry


@pytest.fixture
def validators_registry(session: Session) -> Iterable[ValidatorsRegistry]:
    yield ValidatorsRegistry(session)


def test_validators_registry(validators_registry: ValidatorsRegistry):
    validator_address = "0xabcdef"

    stake = 1
    provider = "ollama"
    model = "llama3"
    config = {}
    actual_validator = validators_registry.create_validator(
        validator_address, stake, provider, model, config
    )
    assert validators_registry.count_validators() == 1

    assert actual_validator["stake"] == stake
    assert actual_validator["provider"] == provider
    assert actual_validator["model"] == model
    assert actual_validator["config"] == config
    created_at = actual_validator["created_at"]
    validator_id = actual_validator["id"]
    assert datetime.fromisoformat(created_at)

    actual_validators = validators_registry.get_all_validators()

    actual_validator = validators_registry.get_validator(validator_address)

    assert actual_validators == [actual_validator]

    new_stake = 2
    new_provider = "ollama_new"
    new_model = "llama3.1"
    new_config = {"seed": 1, "key": {"array": [1, 2, 3]}}

    actual_validator = validators_registry.update_validator(
        validator_address, 2, new_provider, new_model, new_config
    )

    assert validators_registry.count_validators() == 1

    assert validators_registry.get_validator(validator_address) == actual_validator

    assert actual_validator["stake"] == new_stake
    assert actual_validator["provider"] == new_provider
    assert actual_validator["model"] == new_model
    assert actual_validator["config"] == new_config
    assert actual_validator["id"] == validator_id
    assert actual_validator["created_at"] == created_at

    validators_registry.delete_validator(validator_address)

    assert len(validators_registry.get_all_validators()) == 0
    assert validators_registry.count_validators() == 0
