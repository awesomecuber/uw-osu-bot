import discord

from .. import state
from .test_valid_play import is_valid_play
from ..osu_api import api_helper
from ..osu_api.score import Score


async def check_player_scores(player_id: int) -> list[discord.Embed]:
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

            play_url = f"https://osu.ppy.sh/scores/osu/{valid_play_json['best_id']}"
            description = f"{song_name}: {difficulty_name} ({new_score.sr})"

            user_profile = f"https://osu.ppy.sh/users/{valid_play_json['user_id']}/osu"
            icon_url = valid_play_json["user"]["avatar_url"]

            embed=discord.Embed(title="Top Score!", url=play_url, description=description, color=0x1eff00)
            embed.set_author(name=f"{username}", url=user_profile, icon_url=icon_url)
            embed.add_field(name="ACC", value=f"{new_score.acc * 100:.2f}%", inline=True)
            embed.add_field(name="COMBO", value=f"{new_score.max_combo}/{new_score.max_possible_combo}", inline=True)
            embed.add_field(name="MISSES", value=f"{new_score.misses}x", inline=True)
            embed.set_footer(text=(
                    f"This play has a score of {new_score.calculate_score():.0f}/1000. "
                    f"Taking into map difficulty, this play is worth {new_score.calculate_points():.0f} points!"
                )
            )
            # output.append(
            #     f"{username} got a score of **{new_score.calculate_score():.0f}**"
            #     f" on \"{difficulty_name}\" difficulty ({new_score.sr}*)"
            #     f" of \"{song_name}\"!\n  **ACC**: {new_score.acc * 100:.2f}%\n"
            #     f"  **COMBO**: {new_score.max_combo}/{new_score.max_possible_combo}\n"
            #     f"  **MISSES**: {new_score.misses}x\nThis results in a score of **{new_score.calculate_points():.0f}**."
            # )
            output.append(embed)

    return output
