
def get_total_leaderboards(players):
    message = ""
    player_scores = get_player_scores(players)

    # v[1] is the regularized score, add those up for each map
    final_scores = {
        username: sum([v[1] for v in score_data.values()])
        for (username, score_data) in player_scores.items()
    } # map from username to total score
    for i, (username, total_score) in enumerate(sorted(final_scores.items(), key=lambda x: x[1], reverse=True)):
        message += f"{i+1}. {username} ({total_score:.1f})\n"
    return message


def get_map_leaderboards(players):
    message = ""
    player_scores = get_player_scores(players)
    for mapset_id, mapset_data in state["beatmaps"].items():
        message += f"__{mapset_data['title']}__\n"

        for i, (username, score_data) in enumerate(
                    sorted(player_scores.items(), key=lambda x: x[1][mapset_id][0], reverse=True)
                ):
            score, normalized = score_data[mapset_id]
            message += f"{i+1}. {username}: {score:.1f} (normalized: {normalized:.1f})\n"
        message += "\n"
    return message