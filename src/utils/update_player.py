from ..osu_api import api_helper
from ..osu_api.player import Player


async def update_player(player: Player) -> None:
    player = await api_helper.get_player_by_id(player.player_id)
    player.username = player.username
    player.rank = player.rank
