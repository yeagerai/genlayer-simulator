import re
import json
import aiohttp
import asyncio
from typing import Optional

async def process_streaming_buffer(buffer: str, chunk: str, regex: str) -> str:
    updated_buffer = buffer + chunk
    if regex:
        match = re.search(regex, updated_buffer)
        if match:
            full_match = match.group(0)
            return {'stop': True, 'match': full_match}
    return {'stop': False, 'match': None}

async def stream_http_response(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            async for chunk in response.content.iter_any():
                yield chunk

async def call_ollama(endpoint:str, model_name:str, prompt:str, regex: Optional[str], return_streaming_channel:Optional[asyncio.Queue]) -> str:
    url = f"http://localhost:11434/api/{endpoint}" # TODO: when docker compose change that
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