import json
import os
import warnings
from typing import List

# from hypothesis.errors import NonInteractiveExampleWarning
# from hypothesis_jsonschema import from_schema
from jsonschema import validate, Draft202012Validator

from backend.domain.types import LLMProvider

current_directory = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(current_directory, "providers_schema.json")
default_providers_folder = os.path.join(current_directory, "default_providers")


def get_schema() -> dict:
    with open(schema_file, "r") as f:
        schema = json.loads(f.read())

    Draft202012Validator.check_schema(schema)
    return schema


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


def _to_domain(provider: dict) -> LLMProvider:
    return LLMProvider(
        provider=provider["provider"],
        model=provider["model"],
        config=provider["config"],
    )


# def get_random_provider() -> LLMProvider:
#     schema = get_schema()

#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore", NonInteractiveExampleWarning)
#         value = from_schema(schema).example()

#     validate(instance=value, schema=schema)

#     return _to_domain(value)
