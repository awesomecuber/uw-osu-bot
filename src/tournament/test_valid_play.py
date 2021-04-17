from .tournament_state import TournamentState


def is_valid_play(play_json) -> bool:
    state = TournamentState.instance

    # Is in the pool?
    beatmapset_id = play_json["beatmap"]["beatmapset_id"]
    if beatmapset_id not in state.tournamentmaps:
        return False
    tournament_map = state.tournamentmaps[beatmapset_id]

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
