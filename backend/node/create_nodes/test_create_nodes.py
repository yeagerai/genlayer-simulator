import os
from create_nodes import (
    get_default_config_for_providers_and_nodes,
)


def test_get_default_config_for_providers_and_nodes():
    out = get_default_config_for_providers_and_nodes()

    assert isinstance(out, dict)
    assert "providers" in out
    assert "provider_weights" in out["providers"]
    assert "node_defaults" in out


def test():
    from jsf import JSF

    current_directory = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(current_directory, "providers_schema.json")
    faker = JSF.from_json(schema_file)

    fake_json = faker.generate()

    print(fake_json)
