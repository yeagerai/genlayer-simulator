import os
from backend.node.create_nodes.providers import get_default_providers


def old_test_get_default_config_for_providers_and_nodes():
    out = get_default_config_for_providers_and_nodes()

    assert isinstance(out, dict)
    assert "providers" in out
    assert "provider_weights" in out["providers"]
    assert "node_defaults" in out


# from hypothesis.errors import NonInteractiveExampleWarning
# from hypothesis_jsonschema import from_schema
# from jsonschema import validate


# @given(from_schema(schema))
# def test1():
#     import warnings

#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore", NonInteractiveExampleWarning)
#         value = from_schema(schema).example()
#     pprint(value)
#     validate(instance=value, schema=schema)
#     print()
#     print("Finished validating")
#     print()


def test_default_providers_valid():
    providers = get_default_providers()

    assert len(providers) > 0
