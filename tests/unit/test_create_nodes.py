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
            10,
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
                LLMProvider(provider="heuristai", model="", config={}),
            ],
            None,
            10,
            {"OPENAI_API_KEY": ""},
            [LLMProvider(provider="ollama", model="llama3.1", config={})],
            id="only ollama available",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="", config={}),
            ],
            None,
            10,
            {"OPENAIKEY": "filled"},
            [
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
            ],
            id="only openai available",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            None,
            10,
            {"OPENAI_API_KEY": "", "HEURISTAI_API_KEY": "filled"},
            [
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            id="only heuristai",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="ollama", model="llama3.1", config={}),
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            None,
            10,
            {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
            [
                LLMProvider(provider="ollama", model="llama3.1", config={}),
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            id="all available",
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

    assert set(result).issubset(set(expected))
