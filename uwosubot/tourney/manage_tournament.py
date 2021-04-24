import re

from .tournament_map import TournamentMap
from .. import state
from ..osu_api import api_helper


async def start_tournament(mapcodes: list[str]) -> None:
    # update ranks
    await state.tournament.update_ranks()

    # update beatmaps
    new_tournamentmaps = {}
    mapcode_datas = [parse_code(mapcode) for mapcode in mapcodes]
    beatmapset_ids = [mapcode_data[0] for mapcode_data in mapcode_datas]
    beatmapsets = await api_helper.get_beatmapsets(beatmapset_ids)
    for i in range(len(mapcodes)):
        new_tournamentmaps[beatmapset_ids[i]] = TournamentMap(beatmapsets[i], mapcode_datas[i][1])
    state.tournament.tournamentmaps = new_tournamentmaps

    # reset scores
    for person in state.tournament.get_all_people():
        person.reset_scores()


def parse_code(mapcode: str) -> tuple[int, list[str]]:
    print(mapcode)
    beatmapset_id = int(re.search(r"^\d+", mapcode).group(0))
    mods = get_pairs(re.search(r"[A-Z]+$", mapcode).group(0))
    return beatmapset_id, mods


def get_pairs(s: str) -> list[str]:
    char_list = list(s)
    output = []
    current = ""
    while len(char_list) > 0:
        current += char_list.pop(0)
        if len(current) >= 2:
            output.append(current)
            current = ""
    return output


def stop_tournament() -> None:
    state.tournament.beatmaps = {}
    for person in state.tournament.get_all_people():
        person.reset_scores()
