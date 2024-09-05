from backend.node.create_nodes.providers import (
    create_random_providers,
    get_default_providers,
)


def test_default_providers_valid():
    providers = get_default_providers()

    assert len(providers) > 0


def test_create_random_providers():
    # Note: testing this is very slow, so we only test it once
    create_random_providers(1)
