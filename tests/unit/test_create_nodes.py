import pytest
from backend.domain.types import LLMProvider
from backend.node.create_nodes.create_nodes import random_validator_config


@pytest.mark.parametrize(
    "available_ollama_models,stored_providers,limit_providers,limit_models,amount,environ,expected",
    [
        pytest.param(
            ["llama3"],
            [LLMProvider(provider="ollama", model="llama3", config={})],
            None,
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
            None,
            10,
            {"OPENAI_API_KEY": ""},
            [LLMProvider(provider="ollama", model="llama3.1", config={})],
            id="only ollama available",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="ollama", model="llama3", config={}),
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="", config={}),
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            ["openai"],
            None,
            10,
            {"OPENAIKEY": "filled"},
            [
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
            ],
            id="only openai",
        ),
        pytest.param(
            ["llama3", "llama3.1"],
            [
                LLMProvider(provider="openai", model="gpt-4", config={}),
                LLMProvider(provider="openai", model="gpt-4o", config={}),
                LLMProvider(provider="heuristai", model="a", config={}),
                LLMProvider(provider="heuristai", model="b", config={}),
            ],
            ["heuristai"],
            ["a"],
            10,
            {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
            [
                LLMProvider(provider="heuristai", model="a", config={}),
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
    available_ollama_models,
    stored_providers,
    limit_providers,
    limit_models,
    amount,
    environ,
    expected,
):
    result = random_validator_config(
        lambda: available_ollama_models,
        lambda: stored_providers,
        limit_providers,
        limit_models,
        amount,
        environ,
    )

    assert set(result).issubset(set(expected))


@pytest.mark.parametrize(
    "available_ollama_models,stored_providers,limit_providers,limit_models,amount,environ,exception",
    [
        pytest.param(
            [],
            [LLMProvider(provider="ollama", model="llama3", config={})],
            ["heuristai", "openai"],
            None,
            10,
            {},
            ValueError,
            id="no match",
        ),
        pytest.param(
            [],
            [LLMProvider(provider="ollama", model="llama3", config={})],
            ["ollama"],
            None,
            10,
            {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
            Exception,
            id="no intersection",
        ),
    ],
)
def test_random_validator_config_fail(
    available_ollama_models,
    stored_providers,
    limit_providers,
    limit_models,
    amount,
    environ,
    exception,
):
    with pytest.raises(exception):
        random_validator_config(
            result=random_validator_config(
                lambda: available_ollama_models,
                lambda: stored_providers,
                limit_providers,
                limit_models,
                amount,
                environ,
            )
        )
