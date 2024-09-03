import os
from create_nodes import (
    get_default_config_for_providers_and_nodes,
)


def old_test_get_default_config_for_providers_and_nodes():
    out = get_default_config_for_providers_and_nodes()

    assert isinstance(out, dict)
    assert "providers" in out
    assert "provider_weights" in out["providers"]
    assert "node_defaults" in out


current_directory = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(current_directory, "providers_schema.json")

import json

from pprint import pprint

with open(schema_file, "r") as f:
    schema = json.loads(f.read())


from hypothesis import given
from hypothesis_jsonschema import from_schema


@given(from_schema(schema))
def test1(value):
    pprint(value)


def fadstest():
    # TODO: https://github.com/json-schema-faker/json-schema-faker/tree/master/docs is better at generating fake data. Can we run JavaScript in Python?
    # TODO: test https://github.com/python-jsonschema/hypothesis-jsonschema

    from jsf import JSF
    from jsonschema import validate

    faker = JSF.from_json(schema_file)

    pprint(fake_json)

    pprint(from_schema(schema).example())
    # validate(instance=fake_json, schema=schema)
