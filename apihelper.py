import itertools
import pickle

import asyncio
import json
import aiohttp

import config

URL = "https://osu.ppy.sh/api/"

async def regen_token():
    async with aiohttp.ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "grant_type": "client_credentials",
            "scope": "public"
        }) as response:
            write_file = open("access_token", "wb")
            pickle.dump((await response.json())["access_token"], write_file)
            write_file.close()

async def _get_ranked_beatmapsets(mode_num, *sql_dates):
    with open("access_token", "rb") as f:
        token = pickle.load(f)
    all_maps = []
    async with aiohttp.ClientSession() as session:
        for date in sql_dates:
            cur_page = 1
            while True:
                async with session.get(
                        f"{URL}v2/beatmapsets/search",
                        params={
                            "m": mode_num,
                            "s": "ranked",
                            "q": f"created={date}",
                            "page": cur_page
                        },
                        headers={
                            "Authorization": f"Bearer {token}"
                        }) as response:
                    res = await response.json()
                    all_maps.extend(res["beatmapsets"])
                    cur_page += 1
                    if len(res["beatmapsets"]) < 50: # last page
                        break
    return all_maps

async def get_good_sets(mode: str, months: list[str]):
    sql_dates = []
    for month in months:
        date_month, date_year = month.split("/")
        if len(date_month) == 1:
            date_month = "0" + date_month
        sql_dates.append(f"20{date_year}-{date_month}")

    if mode == "standard":
        mode_id = 0
    elif mode == "mania":
        mode_id = 1

    beatmapsets = await _get_ranked_beatmapsets(mode_id, *sql_dates)

    # maps beatmapset_id to a list of the difficulty of each map
    bmsdiffs = {bms["id"]: [bm["difficulty_rating"] for bm in bms["beatmaps"]] for bms in beatmapsets}
    bmsdiffs = {k:v for (k, v) in bmsdiffs.items() if len(v) >= 5 and max(v) >= 6}
    return list(bmsdiffs.keys())

async def get_rank_username_id(username):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + "get_user",
                params={
                    "k": config.api_key,
                    "u": username,
                    "m": 0,
                    "type": "string"
                }) as response:
            user = await response.json()
            if len(user) == 0:
                raise Exception("That name doesn't exist!")
            user = user[0]
            return int(user["pp_rank"]), user["username"], user["user_id"]

async def get_username(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + "get_user",
                params={
                    "k": config.api_key,
                    "u": id,
                    "m": 0,
                    "type": "id"
                }) as response:
            user = await response.json()
            if len(user) == 0:
                raise Exception("That name doesn't exist!")
            username: str = user[0]["username"]
            if "_" in username:
                underscore_index = username.index("_")
                username = username[:underscore_index] + "\\" + username[underscore_index:]
            return username

async def get_recent(id):
    with open("access_token", "rb") as f:
        token = pickle.load(f)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{URL}v2/users/{id}/scores/recent",
                headers={
                    "Authorization": f"Bearer {token}"
                }) as response:
            scores = await response.json()
            return scores

if __name__ == "__main__":
    asyncio.run(regen_token())
    maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print("a")