# library imports
import asyncio

# file imports
import api_request
import api_urls
import token_handler


async def regen_token():
    async with api_request.get_token() as token:
        token_handler.set_token(token)


async def get_player(username):
    url = api_urls.user_by_username(username)
    async with api_request.get(url, {"key": "username"}) as user:
        user_rank = int(user["statistics"]["global_rank"])
        user_username = user["username"]
        user_id = user["id"]
        return user_rank, user_username, user_id


async def get_username(player_id):
    url = api_urls.user_by_id(player_id)
    async with api_request.get(url, {"key": "id"}) as user:
        return user["username"]


async def get_recent(player_id):
    url = api_urls.recent_scores_by_id(player_id)
    return await api_request.get(url, {})


async def get_beatmap_names(beatmapset_ids):
    urls = [api_urls.beatmapset(beatmapset_id) for beatmapset_id in beatmapset_ids]
    async with api_request.get_many(urls, [{} for _ in urls]) as beatmaps:
        return [beatmap["title"] for beatmap in beatmaps]


if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmap_names([294227, 480669])))
