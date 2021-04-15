# library imports
import asyncio

# file imports
import api_request
import api_urls
import token_handler
from ..utils import modes


async def regen_token():
    async with api_request.get_token() as token:
        token_handler.set_token(token)


def _generate_sql_dates(months: list[str]):
    sql_dates = []
    for month in months:
        date_month, date_year = month.split("/")
        if len(date_month) == 1:
            date_month = "0" + date_month
        sql_dates.append(f"20{date_year}-{date_month}")
    return sql_dates


async def get_good_sets(mode: str, months: list[str]):
    sql_dates = _generate_sql_dates(months)
    mode_id = modes.get_id(mode)
    beatmapsets = await api_request.get_ranked_beatmapsets(mode_id, sql_dates)

    good_sets = []
    for beatmapset in beatmapsets:
        beatmaps = beatmapset["beatmaps"]
        max_star_rating = max([beatmap["difficulty_rating"] for beatmap in beatmaps])
        if len(beatmaps) >= 5 and max_star_rating >= 6:
            good_sets.append(beatmapset["id"])
    return good_sets


async def get_rank_username_id(username):
    url = api_urls.user_by_username(username)
    async with api_request.get(url, {"key": "username"}) as user:
        user_rank = int(user["statistics"]["global_rank"])
        user_username = user["username"]
        user_id = user["id"]
        return user_rank, user_username, user_id


async def get_username(id):
    url = api_urls.user_by_id(id)
    async with api_request.get(url, {"key": "id"}) as user:
        return user["username"]


async def get_recent(id):
    url = api_urls.recent_scores_by_id(id)
    return await api_request.get(url, {})


async def get_beatmap_names(ids):
    urls = [api_urls.beatmapset(id) for id in ids]
    async with api_request.get_many(urls, [{} for _ in urls]) as maps:
        return [map["title"] for map in maps]

if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmap_names(294227, 480669)))
