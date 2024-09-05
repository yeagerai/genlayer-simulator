from hypothesis import HealthCheck, given, settings
from hypothesis.errors import HypothesisDeprecationWarning
from hypothesis_jsonschema import from_schema
from backend.node.create_nodes.providers import (
    get_default_providers,
    get_random_provider,
    get_schema,
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


@settings(max_examples=1)
@given(
    from_schema(get_schema()),
)
def test_random_provider(value):
    print()
    print(value)
    print()
    # assert False
    assert value is not None


return_value = None


def custom():
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", HypothesisDeprecationWarning)

        @settings(max_examples=1, suppress_health_check=(HealthCheck.return_value,))
        @given(
            from_schema(get_schema()),
        )
        def inner(value):
            global return_value
            return_value = value

    inner()
    return return_value


print(custom())
print(custom())
print(custom())
print(custom())
