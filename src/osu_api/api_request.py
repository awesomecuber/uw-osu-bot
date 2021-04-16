from typing import Any, Dict, List

import aiohttp

import api_config
import api_urls
import http_request
import token_handler
from beatmapset import Beatmapset


async def get_token() -> str:
    data = {
        "client_id": api_config.client_id(),
        "client_secret": api_config.client_secret(),
        "grant_type": "client_credentials",
        "scope": "public"
    }

    async with http_request.post(api_urls.token(), data) as result:
        return result["access_token"]


def headers() -> Dict[str, str]:
    token = token_handler.get_token()
    return {"Authorization": f"Bearer {token}"}


async def get(url: str, params: Dict[str, Any]) -> str:
    async with http_request.get(url, headers(), params) as result:
        return result


async def get_many(urls: List[str], params: List[Dict[str, Any]]) -> str:
    async with http_request.get_many(urls, [headers() for _ in urls], params) as result:
        return result


async def get_ranked_beatmapsets(mode_num: int, sql_dates: List[str]) -> List[Beatmapset]:
    results = []
    async with aiohttp.ClientSession() as session:
        for date in sql_dates:
            cur_page = 1
            while True:
                params = {
                    "m": mode_num,
                    "s": "ranked",
                    "q": f"created={date}",
                    "page": cur_page
                }
                async with session.get("beatmapsets/search", params=params, headers=headers()) as response:
                    res = await response.json()
                    for beatmapset_json in res["beatmapsets"]:
                        results.append(Beatmapset(beatmapset_json))
                    cur_page += 1
                    if len(res["beatmapsets"]) < 50:  # last page
                        break
    return results
