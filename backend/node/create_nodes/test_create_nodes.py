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


from hypothesis.errors import NonInteractiveExampleWarning
from hypothesis_jsonschema import from_schema
from jsonschema import validate


# @given(from_schema(schema))
def test1():
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", NonInteractiveExampleWarning)
        value = from_schema(schema).example()
    pprint(value)
    validate(instance=value, schema=schema)
    print()
    print("Finished validating")
    print()


def fadstest():
    # TODO: https://github.com/json-schema-faker/json-schema-faker/tree/master/docs is better at generating fake data. Can we run JavaScript in Python?
    # TODO: test https://github.com/python-jsonschema/hypothesis-jsonschema
    pass
    # from jsf import JSF

    # faker = JSF.from_json(schema_file)

    # pprint(fake_json)

    # pprint(from_schema(schema).example())
    # validate(instance=fake_json, schema=schema)
