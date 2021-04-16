from typing import Optional

from ..osu_api import api_helper
from ..osu_api.player import Player
from person import Person
from tournament_state import TournamentState


def is_registered(player_id: int) -> bool:
    state = TournamentState.instance
    return player_id in state.pros or player_id in state.amateurs


def register(discord_id: int, player_name: str) -> str:
    state = TournamentState.instance

    # Test if discord account is already registered
    registered_discord_id = get_discord_id_by_player_name(player_name)
    if registered_discord_id is not None:
        return "You're already registered!"

    # Test if player is already registered to another discord account
    registered_player = get_player_by_discord_id(discord_id)
    if registered_player is not None:
        return f"This Discord account has already registered osu! account: {registered_player.username}."

    # Register the player
    player = await api_helper.get_player_by_username(player_name)
    person = Person(discord_id, player)
    state.register(person)

    return f"Successfully registered {player_name}!"


def unregister(discord_id: int) -> str:
    state = TournamentState.instance

    # Check if player is registered
    registered_player = get_player_by_discord_id(discord_id)
    if registered_player is None:
        return "This Discord account has no registered osu! account."

    # Remove player
    player_id = registered_player.player_id
    state.unregister(player_id)

    return f"Successfully unregistered {registered_player.username}!"


def get_player_by_discord_id(discord_id: int) -> Optional[Player]:
    state = TournamentState.instance
    for person in state.pros.values():
        if person.discord_id == discord_id:
            return person.player
    for person in state.amateurs.values():
        if person.discord_id == discord_id:
            return person.player
    return None


def get_discord_id_by_player_name(player_name: str) -> Optional[int]:
    state = TournamentState.instance
    for person in state.pros.values():
        if person.player.username == player_name:
            return person.discord_id
    for person in state.amateurs.values():
        if person.player.username == player_name:
            return person.discord_id
    return None
