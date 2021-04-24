from .. import state
from .test_valid_play import is_valid_play
from ..osu_api import api_helper
from ..osu_api.score import Score


async def check_player_scores(player_id: int) -> list[str]:
    person = state.tournament.get_person_by_player_id(player_id)

    recent_plays_jsons = await api_helper.get_recent(player_id)
    valid_plays_jsons = [play_json for play_json in recent_plays_jsons if is_valid_play(play_json)]

    output = []

    for valid_play_json in valid_plays_jsons:
        beatmapset_id = valid_play_json["beatmap"]["beatmapset_id"]

        new_score = Score(valid_play_json)

        current_play: Score = person.scores[beatmapset_id]
        if current_play.calculate_points() < new_score.calculate_points():
            person.scores[beatmapset_id] = new_score

            username = person.player.username
            difficulty_name = valid_play_json['beatmap']['version']
            song_name = valid_play_json['beatmapset']['title_unicode']
            output.append(
                f"{username} got {new_score.pp}pp on \"{difficulty_name}\" difficulty ({new_score.sr}*)"
                f" of \"{song_name}\"! This results in a score of {new_score.calculate_points():.1f}."
            )

    return output
