# backend/node/genvm/llms.py

import os
import re
import json
import aiohttp
import asyncio
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
            return {"stop": True, "match": full_match}
    return {"stop": False, "match": None}


async def stream_http_response(url, data):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(verify_ssl=False)
    ) as session:
        async with session.post(url, json=data, ssl=False) as response:
            async for chunk in response.content.iter_any():
                yield chunk


async def call_ollama(
    model_config: dict,
    prompt: str,
    regex: Optional[str],
    return_streaming_channel: Optional[asyncio.Queue],
) -> str:
    url = get_ollama_url("generate")

    data = {"model": model_config["model"], "prompt": prompt}

    for name, value in model_config["config"].items():
        data[name] = value

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
            if result["stop"]:
                return result["match"]


async def call_openai(
    model_config: dict,
    prompt: str,
    regex: Optional[str],
    return_streaming_channel: Optional[asyncio.Queue],
) -> str:
    client = get_openai_client(os.environ.get("OPENAIKEY"))
    # TODO: OpenAI exceptions need to be caught here
    stream = get_openai_stream(client, prompt, model_config)

    return await get_openai_output(stream, regex, return_streaming_channel)


async def call_heuristai(
    model_config: dict,
    prompt: str,
    regex: Optional[str],
    return_streaming_channel: Optional[asyncio.Queue],
) -> str:
    client = get_openai_client(
        os.environ.get("HEURISTAIAPIKEY"), os.environ.get("HEURISTAIURL")
    )
    stream = get_openai_stream(client, prompt, model_config)
    # TODO: Get the line below working
    # return await get_openai_output(stream, regex, return_streaming_channel)
    output = ""
    for chunk in stream:
        # raise Exception(chunk.json(), dir(chunk), chunk.choices[0].delta.content)
        try:
            output += chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(chunk.json(), dir(chunk))
    # return stream.choices[0].message.content
    return output


def get_openai_client(api_key: str, url: str = None):
    openai_client = None
    if url:
        openai_client = OpenAI(api_key=api_key, base_url=url)
    else:
        openai_client = OpenAI(api_key=api_key)
    return openai_client


def get_openai_stream(client, prompt, model_config):
    config = model_config["config"]
    if "temperature" in config and "max_tokens" in config:
        return client.chat.completions.create(
            model=model_config["model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
        )
    else:
        return client.chat.completions.create(
            model=model_config["model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )


async def get_openai_output(stream, regex, return_streaming_channel):
    buffer = ""
    for chunk in stream:
        chunk_str = chunk.choices[0].delta.content
        if chunk_str is not None:
            if return_streaming_channel is not None:
                await return_streaming_channel.put(chunk_str)
                continue
            result = await process_streaming_buffer(buffer, chunk_str, regex)
            buffer += chunk_str
            if result["stop"]:
                return result["match"]
            else:
                if return_streaming_channel is not None:
                    await return_streaming_channel.put({"done": True})
                if "done" in chunk_str:
                    return buffer
        else:
            return buffer


def get_ollama_url(endpoint: str) -> str:
    return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"
