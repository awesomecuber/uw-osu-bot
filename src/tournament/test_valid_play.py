import tournament_state


def is_valid_play(play_json) -> bool:
    state = tournament_state.get_state()

    # Is in the pool?
    beatmapset_id = str(play_json["beatmap"]["beatmapset_id"])
    if beatmapset_id not in state.beatmaps:
        return False
    tournament_map = state.beatmaps.get(beatmapset_id)

    # Was up for pp?
    if play_json["pp"] is None:
        return False

    required_mods = tournament_map.mods
    play_mods = play_json["mods"]

    # NM
    if required_mods == ["NM"]:
        return len(play_mods) == 0

    # Count must be the same
    if len(required_mods) != len(play_mods):
        return False

    # Each play mod must be a tournament mod
    for play_mod in play_mods:
        if play_mod not in required_mods:
            return False

    return True