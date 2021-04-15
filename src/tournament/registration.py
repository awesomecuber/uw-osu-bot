from ..osu_api import api_helper
from person import Person
import tournament_state


def is_registered(player_id) -> bool:
    state = tournament_state.get_state()
    return player_id in state.pros or player_id in state.amateurs


def register(discord_id, player_name) -> bool:
    state = tournament_state.get_state()

    identity = get_player_by_discord_id(discord_id)
    if len(identity) != 0:
        username = await api_helper.get_username(identity[0])
        await ctx.channel.send(
            f"This Discord account has already registered osu! account: {username}."
        )
        return False

    player = await api_helper.get_player(player_name)
    if is_registered(player.id):
        await ctx.channel.send("You're already registered!")
        return False

    person = Person(discord_id, player)
    state.register(person)

    update_state()
    await update_display()
    await update_detailed_display()
    await ctx.channel.send(f"Successfully registered {player_name}!")
    return True
