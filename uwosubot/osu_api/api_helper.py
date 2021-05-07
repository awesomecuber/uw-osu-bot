import asyncio

from . import api_request, token_handler
from .beatmapset import Beatmapset
from .player import Player

BASE_URL = "https://osu.ppy.sh/api/v2/"

async def regen_token() -> None:
    token = await api_request.get_token()
    token_handler.set_token(token)


async def get_player_by_username(username: str) -> Player:
    url = BASE_URL + f"users/{username}/osu"
    player_json = await api_request.get(url, {"key": "username"})
    return Player(player_json)


async def get_player_by_id(player_id: int) -> Player:
    url = BASE_URL + f"users/{player_id}"
    player_json = await api_request.get(url, {"key": "id"})
    return Player(player_json)


async def get_recent(player_id: int):
    url = BASE_URL + f"users/{player_id}/scores/recent"
    return await api_request.get(url, {"mode": "osu"})


async def get_beatmapsets(beatmapset_ids: list[int]) -> list[Beatmapset]:
    urls = [BASE_URL + f"beatmapsets/{beatmapset_id}" for beatmapset_id in beatmapset_ids]
    beatmapset_jsons = await api_request.get_many(urls, [{} for _ in urls])
    return [Beatmapset(beatmapset_json) for beatmapset_json in beatmapset_jsons]


if __name__ == "__main__":
    asyncio.run(regen_token())
    # maps = asyncio.run(get_good_sets("standard", ["1/21", "2/21"]))
    print(asyncio.run(get_beatmapsets([294227, 480669])))
