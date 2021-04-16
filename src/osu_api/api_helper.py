import asyncio

import api_request
import api_urls
import token_handler
from beatmapset import Beatmapset
from player import Player


async def regen_token() -> None:
    async with api_request.get_token() as token:
        token_handler.set_token(token)


async def get_player_by_username(username: str) -> Player:
    url = api_urls.user_by_username(username)
    async with api_request.get(url, {"key": "username"}) as player_json:
        return Player(player_json)


async def get_player_by_id(player_id) -> Player:
    url = api_urls.user_by_id(player_id)
    async with api_request.get(url, {"key": "id"}) as player_json:
        return Player(player_json)


async def get_recent(player_id):
    url = api_urls.recent_scores_by_id(player_id)
    return await api_request.get(url, {})


async def get_beatmapsets(beatmapset_ids: list) -> list[Beatmapset]:
    urls = [api_urls.beatmapset(beatmapset_id) for beatmapset_id in beatmapset_ids]
    async with api_request.get_many(urls, [{} for _ in urls]) as beatmapset_jsons:
        return [Beatmapset(beatmapset_json) for beatmapset_json in beatmapset_jsons]


if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmapsets([294227, 480669])))
