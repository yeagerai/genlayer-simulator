import os
import re
import json
import aiohttp
import asyncio
from typing import Optional

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

async def call_ollama(endpoint:str, model_name:str, prompt:str, regex: Optional[str], return_streaming_channel:Optional[asyncio.Queue]) -> str:
    url = f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

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