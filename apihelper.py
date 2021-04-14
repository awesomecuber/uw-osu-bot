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

async def _get_ranked_beatmaps(mode_num, *sql_dates):
    async with aiohttp.ClientSession() as session:

        async def do_api_call(sql_date):
            async with session.get(URL + "get_beatmaps",
                    params={
                        "k": config.api_key,
                        "m": mode_num,
                        "since": sql_date
                    }) as response:
                beatmaps = await response.json()
                beatmaps = [bm for bm in beatmaps if bm["approved"] == "1"]
                return beatmaps

        beatmap_fragments = await asyncio.gather(*[do_api_call(d) for d in sql_dates])
        raw_beatmaps = list(itertools.chain(*beatmap_fragments)) # connect tuple
        return list({bm['beatmap_id']: bm for bm in raw_beatmaps}.values()) # only unique

async def get_good_sets(mode: str, months: list[str]):
    sql_dates = []
    for month in months:
        date_month, date_year = month.split("/")
        if len(date_month) == 1:
            date_month = "0" + date_month
        sql_dates.append(f"20{date_year}-{date_month}-01")
        sql_dates.append(f"20{date_year}-{date_month}-14")

    mode_id = -1
    if mode == "standard":
        mode_id = 0
    elif mode == "mania":
        mode_id = 1

    beatmaps = await _get_ranked_beatmaps(mode_id, *sql_dates)

    beatmap_sets = {} # maps beatmapset_id to a list of the difficulty of each map
    for bm in beatmaps:
        bid = int(bm["beatmapset_id"])
        if bid not in beatmap_sets:
            beatmap_sets[bid] = []
        beatmap_sets[bid].append(float(bm["difficultyrating"]))

    beatmap_sets = {k:v for (k, v) in beatmap_sets.items() if len(v) >= 5 and max(v) >= 6}
    return list(beatmap_sets.keys())

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
    print(asyncio.run(get_username(5036976)))