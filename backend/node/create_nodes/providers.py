import os
from typing import List
from jsonschema import validate


# TODO: cast providers into some kind of class. We know that all providers have `provider` and `model` keys
def get_default_providers() -> List[dict]:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(current_directory, "providers_schema.json")

    import json

    from pprint import pprint

    with open(schema_file, "r") as f:
        schema = json.loads(f.read())

    default_providers_folder = os.path.join(current_directory, "default_providers")

    files = [
        os.path.join(default_providers_folder, filename)
        for filename in os.listdir(default_providers_folder)
        if filename.endswith(".json")
    ]

    providers = []
    for file in files:
        with open(file, "r") as f:
            providers.append(json.loads(f.read()))

    for provider in providers:
        validate(instance=provider, schema=schema)

    return providers
