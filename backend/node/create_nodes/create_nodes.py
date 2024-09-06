import os
import re
import secrets
from typing import Callable, List
import requests
from numpy.random import default_rng

from dotenv import load_dotenv

from backend.domain.types import LLMProvider

load_dotenv()
rng = default_rng(secrets.randbits(128))

empty_provider_key_regex = r"^(<add_your_.*_api_key_here>|)$"
provider_key_names_suffix = ["_API_KEY", "KEY", "APIKEY"]


def get_available_ollama_models(get_ollama_url: Callable[[str], str]) -> List[str]:
    ollama_models_result = requests.get(get_ollama_url("tags")).json()
    installed_ollama_models = []
    for ollama_model in ollama_models_result["models"]:
        # "llama3:latest" => "llama3"
        installed_ollama_models.append(ollama_model["name"].split(":")[0])
    return installed_ollama_models


def random_validator_config(
    get_available_ollama_models: Callable[[], str],
    get_stored_providers: Callable[[], List[LLMProvider]],
    provider_names: set[str] = None,
    amount: int = 1,
    environ: dict[str, str] = os.environ,
) -> List[LLMProvider]:
    providers_to_use = get_stored_providers()

    if provider_names:
        providers_to_use = [
            provider
            for provider in providers_to_use
            if provider.provider in provider_names
        ]
        # stored_providers_to_use

    if not providers_to_use:
        raise ValueError(
            f"Requested providers '{provider_names}' do not match any stored providers. Please review your stored providers."
        )

    # Ollama is the only provider which is not OpenAI compliant, thus it gets its custom logic
    # To add more non-OpenAI compliant providers, we'll need to add more custom logic here or refactor the provider's schema to allow general configurations
    available_ollama_models = get_available_ollama_models()

    providers_to_use = [
        provider
        for provider in providers_to_use
        if provider.provider != "ollama" or provider.model in available_ollama_models
    ]

    def filter_by_available_key(provider: LLMProvider) -> bool:
        if provider.provider == "ollama":
            return True
        provider_key_names = [
            provider.provider.upper() + suffix for suffix in provider_key_names_suffix
        ]
        for provider_key_name in provider_key_names:
            if not re.match(
                empty_provider_key_regex, environ.get(provider_key_name, "")
            ):
                return True

        return False

    providers_to_use = list(filter(filter_by_available_key, providers_to_use))

    if not providers_to_use:
        raise Exception("No providers avaliable.")

    # heuristic_models_result = requests.get(os.environ['HEURISTAIMODELSURL']).json()
    # heuristic_models = []
    # for entry in heuristic_models_result:
    #    heuristic_models.append(entry['name'])

    return list(rng.choice(providers_to_use, amount))
