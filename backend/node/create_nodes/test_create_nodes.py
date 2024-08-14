from backend.node.create_nodes.create_nodes import (
    get_default_config_for_providers_and_nodes,
)


def test_get_default_config_for_providers_and_nodes():
    out = get_default_config_for_providers_and_nodes()

    assert isinstance(out, dict)
    assert "providers" in out
    assert "provider_weights" in out["providers"]
    assert "node_defaults" in out
