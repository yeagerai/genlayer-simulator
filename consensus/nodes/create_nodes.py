import os
import json
import requests
import numpy as np
from random import random, choice

from database.credentials import get_genlayer_db_connection

from dotenv import load_dotenv
load_dotenv()

def get_ollama_url(endpoint:str) -> str:
    return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

def base_node_json(provider:str, model:str) -> dict:
    return {'provider': provider, 'model': model, 'config':{}}

def num_decimal_places(number:float) -> int:
    fractional_part = number - int(number)
    decimal_places = 0
    while fractional_part != 0:
        fractional_part *= 10
        fractional_part -= int(fractional_part)
        decimal_places += 1
    return decimal_places

def random_validator_config():
    cwd = os.path.abspath(os.getcwd())

    nodes_dir = '/consensus/nodes'

    # make sure the models are avaliable
    result = requests.get(get_ollama_url('tags')).json()
    if not len(result['models']) and os.environ['GENVMOPENAIKEY'] == '<add_your_open_ai_key_here>':
        raise Exception('No models avaliable.')

    # See if they have an OpenAPI key
    available_models = ''
    if os.environ['GENVMOPENAIKEY'] != '<add_your_open_ai_key_here>':
        available_models = os.environ['GENVMOPENAIMODELS']

    # Get a list of avaliable models
    for ollama_model in result['models']:
        # "llama2:latest" => "llama2"
        available_models += ',' + ollama_model['name'].split(':')[0]
    # remove the first ","
    available_models = available_models[1:]

    # Get all the model defaults
    file = open(cwd + nodes_dir + '/defaults.json', 'r')
    contents = json.load(file)[0]

    defaults = contents['defaults']

    ollama_openai_split = defaults['ollama_openai_split']

    # Use OpenAI
    if random() >= ollama_openai_split:
        model = choice(defaults['openai_models'].split(','))
        node_config = base_node_json('openai', model)

    # Use Ollama
    else:
        model = choice(available_models.split(','))
        node_config = base_node_json('ollama', model)

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

    return node_config
