import asyncio
import aiohttp

import json


async def post(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data=data) as response:
            response_json = await response.json()
            return response_json


async def get(url, headers, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response_json = await response.json()
            return response_json


async def get_many(urls, headerss, paramss):
    async with aiohttp.ClientSession() as session:
        result = []

        for i in range(len(urls)):
            async with session.get(urls[i], headers=headerss[i], params=paramss[i]) as response:
                response_json = await response.json()
                result.append(response_json)
        return result
