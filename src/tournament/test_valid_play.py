from . import state


def is_valid_play(play_json) -> bool:
    # Is in the pool?
    beatmapset_id = play_json["beatmap"]["beatmapset_id"]
    tournament_map = state.tournament.get_tournamentmap_by_beatmapset_id(beatmapset_id)
    if tournament_map is None:
        return False

    # Was up for pp?
    if play_json["pp"] is None:
        return False

    required_mods = tournament_map.mods
    play_mods = play_json["mods"]

    # NM
    if len(required_mods) == 1 and required_mods[0] == "NM":
        return len(play_mods) == 0

    # Count must be the same
    if len(required_mods) != len(play_mods):
        return False

    # Each play mod must be a tournament mod
    for play_mod in play_mods:
        if play_mod not in required_mods:
            return False

    return True
