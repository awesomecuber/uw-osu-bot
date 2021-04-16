from ..osu_api import api_helper
from person import Person
import tournament_state


def is_registered(player_id) -> bool:
    state = tournament_state.get_state()
    return player_id in state.pros or player_id in state.amateurs


def register(discord_id, player_name) -> str:
    state = tournament_state.get_state()

    identity = get_player_by_discord_id(discord_id)
    if len(identity) != 0:
        username = await api_helper.get_username(identity[0])
        return f"This Discord account has already registered osu! account: {username}."

    player = await api_helper.get_player_by_username(player_name)
    if is_registered(player.player_id):
        return "You're already registered!"

    person = Person(discord_id, player)
    state.register(person)

    update_state()
    await update_display()
    await update_detailed_display()
    return f"Successfully registered {player_name}!"
