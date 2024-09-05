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


def get_provider_models(
    defaults: dict, provider: str, get_ollama_url: Callable[[str], str]
) -> list:
    if provider == "ollama":
        ollama_models_result = requests.get(get_ollama_url("tags")).json()
        installed_ollama_models = []
        for ollama_model in ollama_models_result["models"]:
            # "llama3:latest" => "llama3"
            installed_ollama_models.append(ollama_model["name"].split(":")[0])
        return installed_ollama_models

    elif provider == "openai":
        return defaults["openai_models"].split(",")

    elif provider == "heuristai":
        return defaults["heuristai_models"].split(",")

    else:
        raise Exception("Provider (" + provider + ") not found")


def get_providers() -> list:
    return ["openai", "ollama", "heuristai"]


def get_default_config_for_providers_and_nodes() -> dict:
    cwd = os.path.abspath(os.getcwd())
    nodes_dir = "/backend/node/create_nodes"
    file = open(cwd + nodes_dir + "/defaults.json", "r")
    config = json.load(file)[0]
    file.close()
    return config


def get_config_with_specific_providers(config, providers: list) -> dict:
    if len(providers) > 0:
        default_providers_weights = config["providers"]["provider_weights"]

        # Rebuild the dictionary with only the desired keys
        config["providers"]["provider_weights"] = {
            provider: weight
            for provider, weight in default_providers_weights.items()
            if provider in providers
        }
    return config


def get_options(provider, contents):
    options = None
    for node_default in contents["node_defaults"]:
        if node_default["provider"] == provider:
            options = node_default["options"]
    if not options:
        raise Exception(provider + " is not specified in node_defaults")
    return options


def num_decimal_places(number: float) -> int:
    fractional_part = number - int(number)
    decimal_places = 0
    while fractional_part != 0:
        fractional_part *= 10
        fractional_part -= int(fractional_part)
        decimal_places += 1
    return decimal_places


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

    # default_config = get_default_config_for_providers_and_nodes()
    # config = get_config_with_specific_providers(default_config, providers)
    # ollama_models = get_provider_models({}, "ollama", get_ollama_url)

    # See if they have an the provider's keys.

    # TODO: when should we check which models are available? Maybe when filling up the database? Should we check every time?
    # TODO: this methods for checking the providers are decoupled from the actual configuration and schema of the providers. This means that modifications need to be done in two places.
    ollama_models = [
        provider.model for provider in provider_names if provider.provider == "ollama"
    ]
    if (
        not len(ollama_models)
        and re.match(default_provider_key_regex, os.environ.get("OPENAIKEY", ""))
        and re.match(default_provider_key_regex, os.environ.get("HEURISTAIAPIKEY", ""))
    ):
        raise Exception("No providers avaliable.")

    # heuristic_models_result = requests.get(os.environ['HEURISTAIMODELSURL']).json()
    # heuristic_models = []
    # for entry in heuristic_models_result:
    #    heuristic_models.append(entry['name'])

    # provider = get_random_provider_using_weights(config["providers"], get_ollama_url)
    # options = get_options(provider, config)

    # raise Exception("Provider " + provider + " is not specified in defaults")

    return create_random_providers(amount)  # TODO: filter by provider and availability
