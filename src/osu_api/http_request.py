from typing import Any, Dict

import aiohttp


async def post(url: str, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_json = await response.json()
            return response_json


async def get(url: str, headers: Dict[str, Any], params: Dict[str, Any]):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response_json = await response.json()
            return response_json


async def get_many(urls: list[str], headerss: list[Dict[str, Any]], paramss: list[Dict[str, Any]]) -> list[Any]:
    async with aiohttp.ClientSession() as session:
        result = []

        for i in range(len(urls)):
            async with session.get(urls[i], headers=headerss[i], params=paramss[i]) as response:
                response_json = await response.json()
                result.append(response_json)
        return result
