from ..tournament.tournament_state import TournamentState
from ..utils.calculate_score import calculate_score


def get_total_leaderboards(players):
    player_scores = get_player_scores(players)

    # v[1] is the regularized score, add those up for each map
    final_scores = {
        username: sum([v[1] for v in score_data.values()])
        for (username, score_data) in player_scores.items()
    } # map from username to total score

    message = ""
    for i, (username, total_score) in enumerate(sorted(final_scores.items(), key=lambda x: x[1], reverse=True)):
        message += f"{i+1}. {username} ({total_score:.1f})\n"
    return message


def get_map_leaderboards(players):
    message = ""
    player_scores = get_player_scores(players)
    for beatmapset in TournamentState.instance.beatmaps.values():
        message += f"__{beatmapset.ascii_name}__\n"

        for i, (username, score_data) in enumerate(
                    sorted(player_scores.items(), key=lambda x: x[1][mapset_id][0], reverse=True)
                ):
            score, normalized = score_data[mapset_id]
            message += f"{i+1}. {username}: {score:.1f} (normalized: {normalized:.1f})\n"
        message += "\n"
    return message


# returns map from username to (map id to (score, normalized))
def get_player_scores(players):
    to_return = {}
    for player_data in players.values():
        scores = {}
        for map_id, score_data in player_data["scores"].items():
            scores[map_id] = calculate_score(score_data["pp"], score_data["sr"])
        to_return[player_data["username"]] = scores

    # add in normalized
    best_scores = {}
    for beatmapset_id in TournamentState.instance.beatmaps.values():
        if len(to_return) == 0:
            best_score = 0
        else:
            best_score = max(v[beatmapset_id] for (_, v) in to_return.items())

        if best_score == 0:
            best_score = 1 # to prevent divide by zero
        best_scores[beatmapset_id] = best_score

    for player_name, player_data in to_return.items():
        for map_id, score in player_data.items():
            to_return[player_name][map_id] = (score, 250 * (score / best_scores[map_id]))
    return to_return