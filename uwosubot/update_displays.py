from discord import TextChannel, Message
from discord.ext.commands import Bot

from . import bot_config, leaderboards, state
from .utils.sanitizer import sanitize


async def update_display(bot: Bot) -> None:
    display_channel = bot.get_channel(bot_config.display_channel())
    discord_messages = await get_discord_messages(display_channel, 1)

    if not state.tournament.is_running():
        await discord_messages[0].edit(content="Tourney not currently running!")
        return

    message = make_display_message()
    await discord_messages[0].edit(content=message)


def make_display_message() -> str:
    message = "**REGISTERED**\n"
    pro_names = [sanitize(person.player.username) for person in state.tournament.get_pros()]
    amateur_names = [sanitize(person.player.username) for person in state.tournament.get_amateurs()]
    message += f"Pros: {', '.join(pro_names)}\nAmateurs: {', '.join(amateur_names)}\n"

    message += "\n**BEATMAPS**\n"
    for tournamentmap in state.tournament.get_tournamentmaps():
        beatmapset_id = tournamentmap.beatmapset.beatmapset_id
        beatmapset_name = sanitize(tournamentmap.beatmapset.ascii_name)
        mods_string = "".join(tournamentmap.mods)

        message += f"{mods_string}: <https://osu.ppy.sh/beatmapsets/{beatmapset_id}> ({beatmapset_name})\n"
    message += "\n**PRO STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state.tournament.get_pros())
    message += "\n**AMATEUR STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state.tournament.get_amateurs())

    return message


async def update_detailed_display(bot: Bot) -> None:
    detail_channel: TextChannel = bot.get_channel(bot_config.detail_channel())
    discord_messages = await get_discord_messages(detail_channel, 2)

    if not state.tournament.is_running():
        await discord_messages[0].edit(content="Tourney not currently running!")
        await discord_messages[1].edit(content=".")
        return

    message_pros, message_ams = make_detailed_display_messages()
    await discord_messages[1].edit(content=message_pros)
    await discord_messages[0].edit(content=message_ams)


def make_detailed_display_messages() -> tuple[str, str]:
    message_pros = "**PROS**\n\n"
    message_pros += leaderboards.get_map_leaderboards(state.tournament.get_pros())
    message_ams = "------------------\n**AMATEURS**\n\n"
    message_ams += leaderboards.get_map_leaderboards(state.tournament.get_amateurs())
    return message_pros, message_ams


async def get_discord_messages(channel: TextChannel, number: int) -> list[Message]:
    messages = await channel.history(limit=number).flatten()

    if len(messages) < number:
        for i in range(number - len(messages)):
            await channel.send(f"temp{i+1}")
        messages = await channel.history(limit=number).flatten()

    return messages
