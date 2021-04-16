from test_valid_play import is_valid_play
from ..discord import bot
from ..osu_api import api_helper
from ..osu_api.score import Score
from ..tournament.tournament_state import TournamentState
from ..utils.calculate_points import calculate_points


async def check_player_scores(player_id: int) -> None:
    state = TournamentState.instance

    person = state.get_person_from_player_id(player_id)

    recent_plays_jsons = await api_helper.get_recent(player_id)
    valid_plays_jsons = [play_json for play_json in recent_plays_jsons if is_valid_play(play_json)]

    for valid_play_json in valid_plays_jsons:
        beatmapset_id = valid_play_json["beatmap"]["beatmapset_id"]

        pp = float(valid_play_json["pp"])
        sr = valid_play_json["beatmap"]["difficulty_rating"]
        score = calculate_points(Score(pp, sr))

        current_play = person.scores.get(beatmapset_id)
        if calculate_points(current_play) < score:
            current_play.pp = pp
            current_play.sr = sr

            username = person.player.username
            difficulty_name = valid_play_json['beatmap']['version']
            song_name = valid_play_json['beatmapset']['title_unicode']
            await bot.announce(
                f"{username} got {pp}pp on \"{difficulty_name}\" difficulty ({sr}*) of \"{song_name}\"!"
                f" This results in a score of {score:.1f}."
            )
