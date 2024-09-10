import json
import os
from typing import List

from jsonschema import Draft202012Validator, validate

from backend.domain.types import LLMProvider

current_directory = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(current_directory, "providers_schema.json")
default_providers_folder = os.path.join(current_directory, "default_providers")


def get_schema() -> dict:
    with open(schema_file, "r") as f:
        schema = json.loads(f.read())

    Draft202012Validator.check_schema(schema)
    return schema


def validate_provider(provider: LLMProvider):
    schema = get_schema()
    try:
        validate(instance=provider.__dict__, schema=schema)
    except Exception as e:
        raise ValueError(f"Error validating provider: {e}")


def get_default_providers() -> List[LLMProvider]:
    schema = get_schema()

    files = [
        os.path.join(default_providers_folder, filename)
        for filename in os.listdir(default_providers_folder)
        if filename.endswith(".json")
    ]

    providers = []
    for file in files:
        with open(file, "r") as f:
            provider = json.loads(f.read())
        try:
            validate(instance=provider, schema=schema)
        except Exception as e:
            raise ValueError(f"Error validating file {file}, provider {provider}: {e}")

        providers.append(_to_domain(provider))

    return providers


def get_default_provider_for(provider: str, model: str) -> LLMProvider:
    llm_providers = get_default_providers()
    matches = [
        llm_provider
        for llm_provider in llm_providers
        if llm_provider.provider == provider and llm_provider.model == model
    ]
    if not matches:
        raise ValueError(f"No default provider found for {provider} and {model}")
    if len(matches) > 1:
        raise ValueError(f"Multiple default providers found for {provider} and {model}")


def _to_domain(provider: dict) -> LLMProvider:
    return LLMProvider(
        id=None,
        provider=provider["provider"],
        model=provider["model"],
        config=provider["config"],
        plugin=provider["plugin"],
        plugin_config=provider["plugin_config"],
    )


def create_random_providers(amount: int) -> list[LLMProvider]:
    """
    Not being used at the moment, left here for future reference.
    Creates random providers deriving them from the json schema.
    Internally uses hypothesis to generate the data, which is hacky since it's meant to be a testing library.
    """
    from hypothesis import HealthCheck, given, settings
    from hypothesis.errors import HypothesisDeprecationWarning
    from hypothesis_jsonschema import from_schema
    import warnings

    return_value = []

    with warnings.catch_warnings():  # Catch warnings from hypothesis telling us to not use it for this purpose
        warnings.simplefilter(
            "ignore", HypothesisDeprecationWarning
        )  # Disable the warning about using the deprecated `suppress_health_check` argument

        @settings(
            max_examples=amount, suppress_health_check=(HealthCheck.return_value,)
        )
        @given(
            from_schema(
                get_schema(),
            ),
        )
        def inner(value):
            nonlocal return_value  # Hypothesis `@given` wrapper doesn't allow us to return from the "test" function, so I'm using this closure to return the value
            provider = _to_domain(value)
            validate_provider(provider)
            return_value.append(provider)

    inner()  # Calling the function will fill the return_value list
    return return_value
