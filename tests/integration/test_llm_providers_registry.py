from tests.common.request import payload, post_request_localhost
from tests.common.response import has_success_status


def test_llm_providers():
    provider = {
        "provider": "openai",
        "model": "gpt-4",
        "config": {},
        "plugin": "openai",
        "plugin_config": {"api_key_env_var": "OPENAIKEY", "api_url": None},
    }
    # Create a new provider
    response = post_request_localhost(payload("sim_addProvider", provider)).json()
    assert has_success_status(response)

    provider_id = response["result"]

    updated_provider = {
        "provider": "openai",
        "model": "gpt-4o",
        "config": {},
        "plugin": "openai",
        "plugin_config": {"api_key_env_var": "OPENAIKEY", "api_url": None},
    }
    # Uodate it
    response = post_request_localhost(
        payload("sim_updateProvider", provider_id, updated_provider)
    ).json()
    assert has_success_status(response)

    # Delete it
    response = post_request_localhost(payload("sim_deleteProvider", provider_id)).json()
    assert has_success_status(response)


def test_llm_providers_behavior():
    """
    Test the behavior of LLM providers endpoints by performing the following steps:

    1. Reset the default LLM providers.
    2. Retrieve the list of providers and models.
    3. Extract the first default provider and the ID of the last provider.
    4. Add a new provider using the first default provider's data.
    5. Update the last provider using the first default provider's data.
    6. Delete the newly added provider.

    """
    reset_result = post_request_localhost(
        payload("sim_resetDefaultsLlmProviders")
    ).json()
    assert has_success_status(reset_result)

    response = post_request_localhost(payload("sim_getProvidersAndModels")).json()
    assert has_success_status(response)

    default_providers = response["result"]
    first_default_provider: dict = default_providers[0]
    del first_default_provider["id"]
    last_provider_id = default_providers[-1]["id"]

    # Create a new provider
    response = post_request_localhost(
        payload("sim_addProvider", first_default_provider)
    ).json()
    assert has_success_status(response)

    provider_id = response["result"]

    # Uodate it
    response = post_request_localhost(
        payload("sim_updateProvider", last_provider_id, first_default_provider)
    ).json()
    assert has_success_status(response)

    # Delete it
    response = post_request_localhost(payload("sim_deleteProvider", provider_id)).json()
    assert has_success_status(response)
