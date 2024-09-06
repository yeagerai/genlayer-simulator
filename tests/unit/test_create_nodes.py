import pytest
from backend.domain.types import LLMProvider
from backend.node.create_nodes.create_nodes import random_validator_config


@pytest.mark.parametrize(
    "available_ollama_models,stored_providers,provider_names,amount,environ,expected",
    [
        pytest.param(
            ["llama3"],
            [LLMProvider(provider="ollama", model="llama3", config={})],
            None,
            1,
            {},
            [LLMProvider(provider="ollama", model="llama3", config={})],
            id="only ollama",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="ollama", model="llama3.1", config={}),
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(
                    provider="heuristai", model="meta-llama/llama-2-70b-chat", config={}
                ),
            ],
            None,
            1,
            {"OPENAIKEY": ""},
            [LLMProvider(provider="ollama", model="llama3.1", config={})],
            id="only ollama available",
        ),
    ],
)
def test_random_validator_config(
    available_ollama_models, stored_providers, provider_names, amount, environ, expected
):
    get_stored_providers = lambda: stored_providers

    get_available_ollama_models = lambda: available_ollama_models

    result = random_validator_config(
        get_available_ollama_models,
        get_stored_providers,
        provider_names,
        amount,
        environ,
    )

    assert expected == result
