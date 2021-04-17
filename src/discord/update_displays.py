from typing import Tuple, List

from discord import TextChannel, Message
from discord.ext.commands import Bot

from . import bot_config, leaderboards
from ..tournament.tournament_state import TournamentState


async def update_display(bot: Bot) -> None:
    display_channel = bot.get_channel(bot_config.display_channel())
    discord_messages = await get_discord_messages(display_channel, 1)

    if not TournamentState.instance.is_running():
        await discord_messages[0].edit(content="Tourney not currently running!")
        return

    message = make_display_message()
    await discord_messages[0].edit(content=message)


def make_display_message() -> str:
    state = TournamentState.instance

    message = "**REGISTERED**\n"
    pro_names = [person.player.username for person in state.pros.values()]
    amateur_names = [person.player.username for person in state.pros.values()]
    message += f"Pros: {', '.join(pro_names)}\nAmateurs: {', '.join(amateur_names)}\n"

    message += "\n**BEATMAPS**\n"
    for tournamentmap in state.tournamentmaps.values():
        beatmapset_id = tournamentmap.beatmapset.beatmapset_id
        beatmapset_name = tournamentmap.beatmapset.ascii_name
        message += f"{tournamentmap.mods}: <https://osu.ppy.sh/beatmapsets/{beatmapset_id}> ({beatmapset_name})\n"

    message += "\n**PRO STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(list(state.pros.values()))
    message += "\n**AMATEUR STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(list(state.amateurs.values()))

    return message


async def update_detailed_display(bot: Bot) -> None:
    detail_channel: TextChannel = bot.get_channel(bot_config.detail_channel())
    discord_messages = await get_discord_messages(detail_channel, 2)

    if not TournamentState.instance.is_running():
        await discord_messages[0].edit(content="Tourney not currently running!")
        await discord_messages[1].edit(content=".")
        return

    message_pros, message_ams = make_detailed_display_messages()
    await discord_messages[1].edit(content=message_pros)
    await discord_messages[0].edit(content=message_ams)


def make_detailed_display_messages() -> Tuple[str, str]:
    state = TournamentState.instance
    message_pros = "**PROS**\n\n"
    message_pros += leaderboards.get_map_leaderboards(list(state.pros.values()))
    message_ams = "------------------\n**AMATEURS**\n\n"
    message_ams += leaderboards.get_map_leaderboards(list(state.amateurs.values()))
    return message_pros, message_ams


async def get_discord_messages(channel: TextChannel, number: int) -> List[Message]:
    messages = await channel.history(limit=number).flatten()

    if len(messages) < number:
        for i in range(number - len(messages)):
            await channel.send(f"temp{i+1}")
        messages = await channel.history(limit=number).flatten()

    return messages
