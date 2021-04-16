from discord import NotFound, TextChannel
import bot_config
import leaderboards


async def update_display(bot):
    display_channel = bot.get_channel(bot_config.display_channel())
    try:
        display_message = await display_channel.fetch_message(display_channel.last_message_id)
    except NotFound:
        await display_channel.send("temp")
        display_message = await display_channel.fetch_message(display_channel.last_message_id)

    if len(state["beatmaps"]) == 0:
        await display_message.edit(content="Tourney not currently running!")
        return

    message = "**REGISTERED**\n"
    pro_names = []
    amateur_names = []
    for pro_id in state["pros"]:
        pro_names.append(state["pros"][pro_id]["username"])
    for amateur_id in state["amateurs"]:
        amateur_names.append(state["amateurs"][amateur_id]["username"])
    message += f"Pros: {', '.join(pro_names)}\nAmateurs: {', '.join(amateur_names)}\n"

    message += "\n**BEATMAPS**\n"
    for bmsid, bmsdata in state["beatmaps"].items():
        message += f"{bmsdata['mod']}: <https://osu.ppy.sh/beatmapsets/{bmsid}> ({bmsdata['title']})\n"

    message += "\n**PRO STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state["pros"])
    message += "\n**AMATEUR STANDINGS**\n"
    message += leaderboards.get_total_leaderboards(state["amateurs"])

    await display_message.edit(content=message)


async def update_detailed_display(bot):
    detail_channel: TextChannel = bot.get_channel(bot_config.detail_channel())
    discord_messages = await detail_channel.history(limit=2).flatten()
    if len(discord_messages) == 0:
        await detail_channel.send("temp1")
        await detail_channel.send("temp2")
        discord_messages = await detail_channel.history(limit=2).flatten()
    if len(discord_messages) == 1:
        await detail_channel.send("temp")
        discord_messages = await detail_channel.history(limit=2).flatten()

    if len(state["beatmaps"]) == 0:
        await discord_messages[0].edit(content="Tourney not currently running!")
        await discord_messages[1].edit(content=".")
        return

    message_pros = "**PROS**\n\n"
    message_pros += leaderboards.get_map_leaderboards(state["pros"])
    message_ams = "------------------\n**AMATEURS**\n\n"
    message_ams += leaderboards.get_map_leaderboards(state["amateurs"])

    await discord_messages[1].edit(content=message_pros)
    await discord_messages[0].edit(content=message_ams)