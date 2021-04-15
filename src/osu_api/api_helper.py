# library imports
import asyncio

# file imports
import api_request
import token_handler
from ..utils import modes

URL = "https://osu.ppy.sh/api/v2/"


async def regen_token():
    async with api_request.get_token() as token:
        token_handler.set_token(token)


async def get_good_sets(mode: str, months: list[str]):
    sql_dates = []
    for month in months:
        date_month, date_year = month.split("/")
        if len(date_month) == 1:
            date_month = "0" + date_month
        sql_dates.append(f"20{date_year}-{date_month}")

    mode_id = modes.get_id(mode)

    beatmapsets = await api_request.get_ranked_beatmapsets(mode_id, sql_dates)

    # maps beatmapset_id to a list of the difficulty of each map
    bms_diffs = {bms["id"]: [bm["difficulty_rating"] for bm in bms["beatmaps"]] for bms in beatmapsets}
    bms_diffs = {k: v for (k, v) in bms_diffs.items() if len(v) >= 5 and max(v) >= 6}
    return list(bms_diffs.keys())


async def get_rank_username_id(username):
    url = URL + f"users/{username}/osu"
    async with api_request.get(url, {"key": "username"}) as user:
        user_rank = int(user["statistics"]["global_rank"])
        user_username = user["username"]
        user_id = user["id"]
        return user_rank, user_username, user_id


async def get_username(id):
    url = URL + f"users/{id}"
    async with api_request.get(url, {"key": "id"}) as user:
        return user["username"]


async def get_recent(id):
    return await api_request.get(URL + f"users/{id}/scores/recent", {})


async def get_beatmap_names(*ids):
    urls = [URL + f"beatmapsets/{id}" for id in ids]
    async with api_request.get_many(urls, [{} for _ in urls]) as maps:
        return [map["title"] for map in maps]

if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmap_names(294227, 480669)))
