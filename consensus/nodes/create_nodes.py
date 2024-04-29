import os
import json
import requests
import numpy as np
from random import random, choice, uniform

from dotenv import load_dotenv
load_dotenv()

def get_ollama_url(endpoint:str) -> str:
    return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

def base_node_json(provider:str, model:str) -> dict:
    return {'provider': provider, 'model': model, 'config':{}}

def get_node_defaults():
    cwd = os.path.abspath(os.getcwd())
    nodes_dir = '/consensus/nodes'
    file = open(cwd + nodes_dir + '/defaults.json', 'r')
    contents = json.load(file)[0]
    return contents['defaults']

def get_random_provider_using_weights(defaults):
    # remove providers if no api key
    provider_weights = defaults['provider_weights']
    default_value = '<add_your_open_ai_key_here>'
    if 'GENVMOPENAIKEY' not in os.environ or os.environ['GENVMOPENAIKEY'] == default_value:
        provider_weights.pop('openai')
    if 'HEURISTAIAPIKEY' not in os.environ or os.environ['HEURISTAIAPIKEY'] == default_value:
        provider_weights.pop('heuristai')

    total_weight = sum(provider_weights.values())
    random_num = uniform(0, total_weight)
    
    cumulative_weight = 0
    for key, weight in provider_weights.items():
        cumulative_weight += weight
        if random_num <= cumulative_weight:
            return key

def get_provider_models(defaults:str, provider:str) -> list:

    if provider == 'ollama':
        ollama_models_result = requests.get(get_ollama_url('tags')).json()
        ollama_models = []
        for ollama_model in ollama_models_result['models']:
            # "llama2:latest" => "llama2"
            ollama_models.append(ollama_model['name'].split(':')[0])
        return ollama_models

    elif provider == 'openai':
        return defaults['openai_models'].split(',')

    elif provider == 'heuristai':
        return defaults['heuristai_models'].split(',')

    else:
        raise Exception('Provider ('+provider+') not found')

def get_providers() -> list:
    return ['openai', 'ollama', 'heuristai']

def get_options(provider, contents):
    options = None
    for node_default in contents['node_defaults']:
        if node_default['provider'] == provider:
            options = node_default['options']
    if not options:
        raise Exception(provider + ' is not specified in node_defaults')
    return options

def num_decimal_places(number:float) -> int:
    fractional_part = number - int(number)
    decimal_places = 0
    while fractional_part != 0:
        fractional_part *= 10
        fractional_part -= int(fractional_part)
        decimal_places += 1
    return decimal_places

def random_validator_config():
    defaults = get_node_defaults()

    ollama_models = get_provider_models(defaults, 'ollama')

    if not len(ollama_models) and \
        os.environ['GENVMOPENAIKEY'] == '<add_your_open_ai_key_here>' and \
        os.environ['HEURISTAIAPIKEY'] == '<add_your_heurist_api_key_here>':
        raise Exception('No models avaliable.')

    # See if they have an OpenAPI key
    
    #heuristic_models_result = requests.get(os.environ['HEURISTAIMODELSURL']).json()
    #heuristic_models = []
    #for entry in heuristic_models_result:
    #    heuristic_models.append(entry['name'])

    provider = get_random_provider_using_weights(defaults)

    options = get_options(provider, contents)

    if provider == 'openai':
        openai_model = choice(get_provider_models(defaults, 'openai'))
        node_config = base_node_json('openai', openai_model)

        options = None
        for provider in contents['node_defaults']:
            if provider['provider'] == 'ollama':
                options = provider['options']
        if not options:
            raise Exception('Ollama is not specified in node_defaults')
        
        for option, option_config in options.items():
            # Just pass the string (for "stop")
            if isinstance(option_config, str):
                node_config['config'][option] = option_config
            # Create a random value
            elif isinstance(option_config, dict):
                if random() > defaults['chance_of_default_value']:
                    random_value = None
                    if isinstance(option_config['step'], str):
                        random_value = choice(
                            option_config['step'].split(',')
                        )
                    else:
                        random_value = choice(
                            np.arange(
                                option_config['min'],
                                option_config['max'],
                                option_config['step']
                            )
                        )
                        if isinstance(random_value, np.int64):
                            random_value = int(random_value)
                        if isinstance(random_value, np.float64):
                            random_value = float(random_value)
                        node_config['config'][option] = round(random_value, num_decimal_places(option_config['step']))
                else:
                    pass
            else:
                raise Exception('Option is not a dict or str ('+option+')')
    elif provider == 'ollama':
        node_config = base_node_json('ollama', choice(ollama_models))
        
        for option, option_config in options.items():
            # Just pass the string (for "stop")
            if isinstance(option_config, str):
                node_config['config'][option] = option_config
            # Create a random value
            elif isinstance(option_config, dict):
                if random() > defaults['chance_of_default_value']:
                    random_value = None
                    if isinstance(option_config['step'], str):
                        random_value = choice(
                            option_config['step'].split(',')
                        )
                    else:
                        random_value = choice(
                            np.arange(
                                option_config['min'],
                                option_config['max'],
                                option_config['step']
                            )
                        )
                        if isinstance(random_value, np.int64):
                            random_value = int(random_value)
                        if isinstance(random_value, np.float64):
                            random_value = float(random_value)
                        node_config['config'][option] = round(random_value, num_decimal_places(option_config['step']))
            else:
                raise Exception('Option is not a dict or str ('+option+')')

    elif provider == 'heuristai':
        heuristic_model = choice(get_provider_models(defaults, 'heuristai'))
        node_config = base_node_json('heuristai', heuristic_model)
        for option, option_config in options.items():
            if random() > defaults['chance_of_default_value']:
                random_value = choice(
                    np.arange(
                        option_config['min'],
                        option_config['max'],
                        option_config['step']
                    )
                )
                if isinstance(random_value, np.int64):
                    random_value = int(random_value)
                if isinstance(random_value, np.float64):
                    random_value = float(random_value)
                node_config['config'][option] = round(random_value, num_decimal_places(option_config['step']))

    else:
        raise Exception('Provider ' + provider + ' is not specified in defaults')

    return node_config
