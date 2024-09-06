import os
import json
import re
from typing import Callable, List
import requests

from dotenv import load_dotenv

from backend.domain.types import LLMProvider
from backend.node.create_nodes.providers import create_random_providers

load_dotenv()

default_provider_key_regex = r"^(<add_your_.*_api_key_here>|)$"


def base_node_json(provider: str, model: str) -> dict:
    return {"provider": provider, "model": model, "config": {}}


def get_available_ollama_models(get_ollama_url: Callable[[str], str]) -> List[str]:
    ollama_models_result = requests.get(get_ollama_url("tags")).json()
    installed_ollama_models = []
    for ollama_model in ollama_models_result["models"]:
        # "llama3:latest" => "llama3"
        installed_ollama_models.append(ollama_model["name"].split(":")[0])
    return installed_ollama_models


def random_validator_config(
    get_ollama_url: Callable[[str], str],
    # get_stored_providers: Callable[[], List[LLMProvider]],
    provider_names: List[str] = None,
    amount: int = 1,
) -> List[LLMProvider]:
    provider_names = provider_names or []

    # stored_providers = get_stored_providers()
    stored_providers = []
    providers_to_use = stored_providers

    if len(provider_names) > 0:
        providers_to_use = [
            provider
            for provider in stored_providers
            if provider.provider in provider_names
        ]
    # TODO: this methods for checking the providers are decoupled from the actual configuration and schema of the providers. This means that modifications need to be done in two places.

    # TODO: when should we check which models are available? Maybe when filling up the database? Should we check every time since the user can download more models?
    available_ollama_models = get_available_ollama_models(get_ollama_url)

    is_openai_available = not re.match(
        default_provider_key_regex, os.environ.get("OPENAIKEY", "")
    )
    is_heuristai_available = not re.match(
        default_provider_key_regex, os.environ.get("HEURISTAIAPIKEY", "")
    )

    # Check for providers' keys.
    if not (available_ollama_models or is_openai_available or is_heuristai_available):
        raise Exception("No providers avaliable.")

    # heuristic_models_result = requests.get(os.environ['HEURISTAIMODELSURL']).json()
    # heuristic_models = []
    # for entry in heuristic_models_result:
    #    heuristic_models.append(entry['name'])

    # provider = get_random_provider_using_weights(config["providers"], get_ollama_url)
    # options = get_options(provider, config)

    # raise Exception("Provider " + provider + " is not specified in defaults")

    # provider = create_random_providers(amount)

    return create_random_providers(amount)  # TODO: filter by provider and availability
