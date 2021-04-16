import tournament_state


def start_tournament() -> None:
    state = tournament_state.get_state()

    # update ranks
    state.update_ranks()

    # update beatmaps
    beatmap_state = {}

    beatmap_names = await api_helper.get_beatmap_names(*[set_code[:-2] for set_code in set_codes])
    # TODO
    # for set_code, map_name in zip(set_codes, beatmap_names):
    #    beatmap_state[set_code[:-2]] = BeatmapData(title=map_name, mod=set_code[-2:])

    state["beatmaps"] = beatmap_state

    # reset scores
    for person in state.pros:
        person.reset_scores()
    for person in state.amateurs:
        person.reset_scores()


def stop_tournament() -> None:
    state["beatmaps"] = {}
    for player_data in (state["pros"] | state["amateurs"]).values():
        player_data["scores"] = {}