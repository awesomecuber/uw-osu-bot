from discord import NotFound, TextChannel
import bot_config
import leaderboards

from ..tournament.tournament_state import TournamentState


async def update_display(bot):
    display_channel = bot.get_channel(bot_config.display_channel())
    try:
        display_message = await display_channel.fetch_message(display_channel.last_message_id)
    except NotFound:
        await display_channel.send("temp")
        display_message = await display_channel.fetch_message(display_channel.last_message_id)

    state = TournamentState.instance

    if not state.is_running():
        await display_message.edit(content="Tourney not currently running!")
        return

    message = "**REGISTERED**\n"
    pro_names = []
    amateur_names = []
    for player in state.pros.values():
        pro_names.append(player.username)
    for player in state.amateurs.values():
        amateur_names.append(player.username)
    message += f"Pros: {', '.join(pro_names)}\nAmateurs: {', '.join(amateur_names)}\n"

    message += "\n**BEATMAPS**\n"
    for tournament_map in state.beatmaps.values():
        beatmapset_id = tournament_map.beatmapset.beatmapset_id
        beatmapset_name = tournament_map.beatmapset.ascii_name
        message += f"{tournament_map.mods}: <https://osu.ppy.sh/beatmapsets/{beatmapset_id}> ({beatmapset_name})\n"

    message += "\n**PRO STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state["pros"])
    message += "\n**AMATEUR STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state["amateurs"])

    await display_message.edit(content=message)


async def update_detailed_display(bot):
    state = TournamentState.instance

    detail_channel: TextChannel = bot.get_channel(bot_config.detail_channel())
    discord_messages = await detail_channel.history(limit=2).flatten()
    if len(discord_messages) == 0:
        await detail_channel.send("temp1")
        await detail_channel.send("temp2")
        discord_messages = await detail_channel.history(limit=2).flatten()
    if len(discord_messages) == 1:
        await detail_channel.send("temp")
        discord_messages = await detail_channel.history(limit=2).flatten()

    if not state.is_running():
        await discord_messages[0].edit(content="Tourney not currently running!")
        await discord_messages[1].edit(content=".")
        return

    message_pros = "**PROS**\n\n"
    message_pros += leaderboards.get_map_leaderboards(state.pros.values())
    message_ams = "------------------\n**AMATEURS**\n\n"
    message_ams += leaderboards.get_map_leaderboards(state.amateurs.values())

    await discord_messages[1].edit(content=message_pros)
    await discord_messages[0].edit(content=message_ams)
