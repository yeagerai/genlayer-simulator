from backend.node.create_nodes.providers import (
    get_default_providers,
    get_random_provider,
)


def test_default_providers_valid():
    providers = get_default_providers()

    assert len(providers) > 0


# Takes too long to run
# def test_get_random_provider():
#     provider = get_random_provider()

#     assert provider is not None
#     assert "provider" in provider
#     assert "model" in provider
