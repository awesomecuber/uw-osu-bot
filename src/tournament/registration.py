from .person import Person
from . import state
from ..osu_api import api_helper


def is_registered(player_id: int) -> bool:
    person = state.tournament.get_person_by_player_id(player_id)
    return person is not None


async def register(discord_id: int, player_name: str) -> str:
    # Test if discord account is already registered
    registered_person = state.tournament.get_person_by_player_name(player_name)
    if registered_person is not None:
        return "You're already registered!"

    # Test if player is already registered to another discord account
    registered_person = state.tournament.get_person_by_discord_id(discord_id)
    if registered_person is not None:
        return f"This Discord account has already registered osu! account: {registered_person.player.username}."

    # Register the player
    player = await api_helper.get_player_by_username(player_name)
    person = Person(discord_id, player)
    state.tournament.register(person)

    return f"Successfully registered {player.username}!"


def unregister(discord_id: int) -> str:
    # Check if person is registered
    registered_person = state.tournament.get_person_by_discord_id(discord_id)
    if registered_person is None:
        return "This Discord account has no registered osu! account."

    # Remove player
    player_id = registered_person.player.player_id
    state.tournament.unregister(player_id)

    return f"Successfully unregistered {registered_person.player.username}!"

