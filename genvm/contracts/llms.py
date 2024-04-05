import os
import re
import json
import aiohttp
import asyncio
import requests
import random
from typing import Optional
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

async def process_streaming_buffer(buffer: str, chunk: str, regex: str) -> str:
    updated_buffer = buffer + chunk
    if regex:
        match = re.search(regex, updated_buffer)
        if match:
            full_match = match.group(0)
            return {'stop': True, 'match': full_match}
    return {'stop': False, 'match': None}

async def stream_http_response(url, data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post(url, json=data, ssl=False) as response:
            async for chunk in response.content.iter_any():
                yield chunk

async def call_ollama(model_name:str, prompt:str, regex: Optional[str], return_streaming_channel:Optional[asyncio.Queue]) -> str:
    url = get_ollama_url('generate')

    data = {"model": model_name, "prompt": prompt}

    buffer = ""
    async for chunk_json in stream_http_response(url, data):
        chunk = json.loads(chunk_json)
        if return_streaming_channel is not None:
            if not chunk.get("done"):
                await return_streaming_channel.put(chunk)
                continue
            else:
                await return_streaming_channel.put({"done": True})
        else:
            if chunk.get("done"):
                return buffer
            result = await process_streaming_buffer(buffer, chunk["response"], regex)
            buffer += chunk["response"]
            if result['stop']:
                return result['match']

async def call_openai(endpoint:str, model_name:str, prompt:str, regex: Optional[str], return_streaming_channel:Optional[asyncio.Queue]) -> str:
    client = OpenAI(
        api_key=os.environ.get("GENVMOPENAIKEY"),
    )
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    buffer = ""
    for chunk in stream:
        chunk_str = chunk.choices[0].delta.content
        if chunk_str is not None:
            if return_streaming_channel is not None:
                await return_streaming_channel.put(chunk_str)
                continue
            result = await process_streaming_buffer(buffer, chunk_str, regex)
            buffer += chunk_str
            if result['stop']:
                return result['match']
            else:
                if return_streaming_channel is not None:
                    await return_streaming_channel.put({'done': True})
                if 'done' in chunk_str:
                    return buffer
        else:
            return buffer

def get_ollama_url(endpoint:str) -> str:
    return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

def get_random_llm_model() -> str:
    # make sure the models are avaliable
    result = requests.get(get_ollama_url('tags')).json()
    if int(os.environ.get('DEBUG')) == 1:
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
    
    model = random.choice(available_models.split(','))

    # Overridden by the developer
    static_llm = os.environ['GENVMSTATICLLM']
    if static_llm:
        if static_llm in available_models:
            model = os.environ['GENVMSTATICLLM']
        else:
            raise Exception(static_llm + ' not avaliable. Choices are ('+available_models+')')

    if int(os.environ.get('DEBUG')) == 1:
        print('--- START: LLM Model ---')
        print(model)
        print('--- END: LLM Model ---')
    
    return model