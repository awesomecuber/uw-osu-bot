import aiohttp

import api_config
import http_request
import token_handler


async def get_token():
    async with http_request.post("https://osu.ppy.sh/oauth/token", {
        "client_id": api_config.client_id(),
        "client_secret": api_config.client_secret(),
        "grant_type": "client_credentials",
        "scope": "public"
    }) as result:
        return result["access_token"]


def headers():
    token = token_handler.get_token()
    return {"Authorization": f"Bearer {token}"}


async def get(url, params):
    async with http_request.get(url, headers(), params) as result:
        return result


async def get_many(urls, params):
    async with http_request.get_many(urls, [headers() for _ in urls], params) as result:
        return result


async def get_ranked_beatmapsets(mode_num, sql_dates):
    all_maps = []
    async with aiohttp.ClientSession() as session:
        for date in sql_dates:
            cur_page = 1
            while True:
                async with session.get(URL + f"beatmapsets/search",
                                       params={
                                           "m": mode_num,
                                           "s": "ranked",
                                           "q": f"created={date}",
                                           "page": cur_page
                                       },
                                       headers=headers()) as response:
                    res = await response.json()
                    all_maps.extend(res["beatmapsets"])
                    cur_page += 1
                    if len(res["beatmapsets"]) < 50:  # last page
                        break
    return all_maps
