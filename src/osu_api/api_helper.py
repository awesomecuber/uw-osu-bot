import asyncio
from typing import List

from . import api_request, api_urls, token_handler
from .beatmapset import Beatmapset
from .player import Player


async def regen_token() -> None:
    token = await api_request.get_token()
    token_handler.set_token(token)


async def get_player_by_username(username: str) -> Player:
    url = api_urls.user_by_username(username)
    player_json = await api_request.get(url, {"key": "username"})
    return Player(player_json)


async def get_player_by_id(player_id: int) -> Player:
    url = api_urls.user_by_id(player_id)
    player_json = await api_request.get(url, {"key": "id"})
    return Player(player_json)


async def get_recent(player_id: int):
    url = api_urls.recent_scores_by_id(player_id)
    return await api_request.get(url, {})


async def get_beatmapsets(beatmapset_ids: List[int]) -> List[Beatmapset]:
    urls = [api_urls.beatmapset(beatmapset_id) for beatmapset_id in beatmapset_ids]
    beatmapset_jsons = await api_request.get_many(urls, [{} for _ in urls])
    return [Beatmapset(beatmapset_json) for beatmapset_json in beatmapset_jsons]


if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmapsets([294227, 480669])))
