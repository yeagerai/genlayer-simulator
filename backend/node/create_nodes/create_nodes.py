import os
import json
import re
from typing import Callable
import requests
import numpy as np
from random import random, choice, uniform

from dotenv import load_dotenv

load_dotenv()

default_provider_key_regex = r"<add_your_.*_api_key_here>"


def base_node_json(provider: str, model: str) -> dict:
    return {"provider": provider, "model": model, "config": {}}


def get_random_provider_using_weights(
    defaults: dict[str], get_ollama_url: Callable[[str], str]
) -> str:
    # remove providers if no api key
    provider_weights: dict[str, float] = defaults["provider_weights"]

    if "openai" in provider_weights and (
        "OPENAIKEY" not in os.environ
        or re.match(default_provider_key_regex, os.environ["OPENAIKEY"])
    ):
        provider_weights.pop("openai")
    if "heuristai" in provider_weights and (
        "HEURISTAIAPIKEY" not in os.environ.get()
        or re.match(os.environ["HEURISTAIAPIKEY"])
    ):
        provider_weights.pop("heuristai")
    if (
        "ollama" in provider_weights
        and get_provider_models({}, "ollama", get_ollama_url) == []
    ):
        provider_weights.pop("ollama")

    if len(provider_weights) == 0:
        raise Exception("No providers avaliable")

    total_weight = sum(provider_weights.values())
    random_num = uniform(0, total_weight)

    cumulative_weight = 0
    for key, weight in provider_weights.items():
        cumulative_weight += weight
        if random_num <= cumulative_weight:
            return key


def get_provider_models(
    defaults: dict, provider: str, get_ollama_url: Callable[[str], str]
) -> list:

    if provider == "ollama":
        ollama_models_result = requests.get(get_ollama_url("tags")).json()
        ollama_models = []
        for ollama_model in ollama_models_result["models"]:
            # "llama3:latest" => "llama3"
            ollama_models.append(ollama_model["name"].split(":")[0])
        return ollama_models

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
    get_ollama_url: Callable[[str], str], providers: list = None
):
    providers = providers or []

    if len(providers) == 0:
        providers = get_providers()
    default_config = get_default_config_for_providers_and_nodes()
    config = get_config_with_specific_providers(default_config, providers)
    ollama_models = get_provider_models({}, "ollama", get_ollama_url)

    if (
        not len(ollama_models)
        and os.environ["OPENAIKEY"] == default_provider_key_regex
        and os.environ["HEURISTAIAPIKEY"] == default_provider_key_regex
    ):
        raise Exception("No providers avaliable.")

    # See if they have an OpenAPI key

    # heuristic_models_result = requests.get(os.environ['HEURISTAIMODELSURL']).json()
    # heuristic_models = []
    # for entry in heuristic_models_result:
    #    heuristic_models.append(entry['name'])

    provider = get_random_provider_using_weights(config["providers"], get_ollama_url)
    options = get_options(provider, config)

    if provider == "openai":
        openai_model = choice(
            get_provider_models(config["providers"], "openai", get_ollama_url)
        )
        node_config = base_node_json("openai", openai_model)

    elif provider == "ollama":
        node_config = base_node_json("ollama", choice(ollama_models))

        for option, option_config in options.items():
            # Just pass the string (for "stop")
            if isinstance(option_config, str):
                node_config["config"][option] = option_config
            # Create a random value
            elif isinstance(option_config, dict):
                if random() > config["providers"]["chance_of_default_value"]:
                    random_value = None
                    if isinstance(option_config["step"], str):
                        random_value = choice(option_config["step"].split(","))
                        node_config["config"][option] = int(random_value)
                    else:
                        random_value = choice(
                            np.arange(
                                option_config["min"],
                                option_config["max"],
                                option_config["step"],
                            )
                        )
                        if isinstance(random_value, np.int64):
                            random_value = int(random_value)
                        if isinstance(random_value, np.float64):
                            random_value = float(random_value)
                        node_config["config"][option] = round(
                            random_value, num_decimal_places(option_config["step"])
                        )
            else:
                raise Exception("Option is not a dict or str (" + option + ")")

    elif provider == "heuristai":
        heuristic_model = choice(
            get_provider_models(config["providers"], "heuristai", get_ollama_url)
        )
        node_config = base_node_json("heuristai", heuristic_model)
        for option, option_config in options.items():
            if random() > config["providers"]["chance_of_default_value"]:
                random_value = choice(
                    np.arange(
                        option_config["min"],
                        option_config["max"],
                        option_config["step"],
                    )
                )
                if isinstance(random_value, np.int64):
                    random_value = int(random_value)
                if isinstance(random_value, np.float64):
                    random_value = float(random_value)
                node_config["config"][option] = round(
                    random_value, num_decimal_places(option_config["step"])
                )

    else:
        raise Exception("Provider " + provider + " is not specified in defaults")

    return node_config
