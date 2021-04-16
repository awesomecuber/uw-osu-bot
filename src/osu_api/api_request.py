from typing import Any, Dict, List

import aiohttp

from . import api_config, api_urls, http_request, token_handler
from .beatmapset import Beatmapset


async def get_token() -> str:
    data = {
        "client_id": api_config.client_id(),
        "client_secret": api_config.client_secret(),
        "grant_type": "client_credentials",
        "scope": "public"
    }

    result = await http_request.post(api_urls.token(), data)
    return result["access_token"]


def headers() -> Dict[str, str]:
    token = token_handler.get_token()
    return {"Authorization": f"Bearer {token}"}


async def get(url: str, params: Dict[str, Any]) -> str:
    result = await http_request.get(url, headers(), params)
    return result


async def get_many(urls: List[str], params: List[Dict[str, Any]]) -> List:
    result = await http_request.get_many(urls, [headers() for _ in urls], params)
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
                response = await session.get("beatmapsets/search", params=params, headers=headers())
                beatmapsets_jsons = response.json()["beatmapsets"]
                for beatmapset_json in beatmapsets_jsons:
                    results.append(Beatmapset(beatmapset_json))
                cur_page += 1
                if len(beatmapsets_jsons) < 50:  # last page
                    break
    return results
