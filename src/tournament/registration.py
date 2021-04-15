from ..osu_api import api_helper
from ..osu_api.score import Score
from person import Person
import tournament_state


def is_registered(player_id):
    state = tournament_state.get_state()
    return state.pros.has_key(player_id) or state.amateurs.has_key(player_id)


def register(discord_id, player_name):
    state = tournament_state.get_state()

    identity = get_player_by_discord_id(discord_id)
    if len(identity) != 0:
        username = await api_helper.get_username(identity[0])
        await ctx.channel.send(
            f"This Discord account has already registered osu! account: {username}."
        )
        return

    player = await api_helper.get_player(player_name)
    if is_registered(player.id):
        await ctx.channel.send("You're already registered!")
        return

    player_data = Person(
        discord_id=discord_id,
        player_name=player_name,
        scores={beatmapset_id: Score(0, 0) for beatmapset_id in state.beatmaps}
    )

    if player.rank < 50000:
        state.pros[id] = player_data
    else:
        state.amateurs[id] = player_data

    update_state()
    await update_display()
    await update_detailed_display()
    await ctx.channel.send(f"Successfully registered {player_name}!")