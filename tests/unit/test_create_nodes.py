from backend.domain.types import LLMProvider
from backend.node.create_nodes.create_nodes import random_validator_config


def test_random_validator_config():
    stored_providers = [LLMProvider(provider="ollama", model="llama3", config={})]
    get_stored_providers = lambda: stored_providers

    get_available_ollama_models = lambda: ["llama3"]

    result = random_validator_config(
        get_available_ollama_models,
        get_stored_providers,
    )

    assert set(result).issubset(set(stored_providers))
