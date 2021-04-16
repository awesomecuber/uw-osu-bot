import re

from tournament_map import TournamentMap
from tournament_state import TournamentState
from ..osu_api import api_helper


def start_tournament(mapcodes) -> None:
    state = TournamentState.instance

    # update ranks
    state.update_ranks()

    # update beatmaps
    new_tournamentmaps = {}
    mapcode_datas = [parse_code(mapcode) for mapcode in mapcodes]
    beatmapset_ids = [mapcode_data[0] for mapcode_data in mapcode_datas]
    beatmapsets = await api_helper.get_beatmapsets(beatmapset_ids)
    for i in range(len(mapcodes)):
        new_tournamentmaps[beatmapset_ids[i]] = TournamentMap(beatmapsets[i], mapcode_datas[i][1])
    state.tournamentmaps = new_tournamentmaps

    # reset scores
    for person in state.pros:
        person.reset_scores()
    for person in state.amateurs:
        person.reset_scores()


def parse_code(mapcode: str) -> tuple[str, list[str]]:
    beatmapset_id = re.search(r"^\d+", mapcode).group(0)
    mods = get_pairs(re.search(r"\a+$", mapcode).group(0))
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
    state = TournamentState.instance

    state.beatmaps = {}
    for person in state.pros.values():
        person.reset_scores()
    for person in state.amateurs.values():
        person.reset_scores()
