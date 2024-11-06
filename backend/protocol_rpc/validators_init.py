import json
from dataclasses import dataclass
from backend.database_handler.accounts_manager import AccountsManager
from backend.database_handler.validators_registry import ValidatorsRegistry
from endpoints import create_validator


@dataclass
class ValidatorConfig:
    stake: int
    provider: str
    model: str
    config: dict | None = None
    plugin: str | None = None
    plugin_config: dict | None = None


def initialize_validators(
    validators_json: str,
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
):
    """
    Idempotently initialize validators from a JSON string by deleting all existing validators and creating new ones.

    Args:
        validators_json: JSON string containing validator configurations
        validators_registry: Registry to store validator information
        accounts_manager: AccountsManager to create validator accounts

    Returns:
        List[ValidatorConfig]: List of initialized validator configurations

    Raises:
        ValueError: If JSON string contains invalid JSON
        KeyError: If required fields are missing in the JSON configuration
    """
    if not validators_json:
        return

    try:
        validators_data = json.loads(validators_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in validators_json: {str(e)}")

    if not isinstance(validators_data, list):
        raise ValueError("validators_json must contain a JSON array")

    validators_registry.delete_all_validators()

    for validator_data in validators_data:
        try:
            validator = ValidatorConfig(**validator_data)

            # Register validator in the registry
            create_validator(
                validators_registry,
                accounts_manager,
                validator.stake,
                validator.provider,
                validator.model,
                validator.config,
                validator.plugin,
                validator.plugin_config,
            )

        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid validator configuration : {str(e)}")
