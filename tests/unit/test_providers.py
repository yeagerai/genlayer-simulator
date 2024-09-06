from backend.node.create_nodes.providers import (
    get_default_providers,
)


def test_default_providers_valid():
    providers = get_default_providers()

    assert len(providers) > 0
