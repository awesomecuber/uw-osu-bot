import datetime
import os
import logging
import pickle
import random
from typing import TypedDict

import discord
from discord.errors import NotFound
from discord.ext import commands, tasks

import apihelper
import config


logging.basicConfig(level=logging.INFO)

# types


class PlayerData(TypedDict):
    discord_id: int
    username: str
    scores: dict[str, int] # beatmapset_id to score

class State(TypedDict):
    pros: dict[str, PlayerData] # user_id to data
    amateurs: dict[str, PlayerData] # user_id to data
    beatmaps: list[str] # beatmapset_ids


bot = commands.Bot(command_prefix="uw!")
state = State(pros={}, amateurs={}, beatmaps=[])


# recurrent tasks

@tasks.loop(minutes=1)
async def score_check():
    # check that tournament is running
    if len(state["beatmaps"]) == 0:
        return

    # print("Start score check:", datetime.datetime.now())
    for id in state["pros"] | state["amateurs"]:
        # print(id, "score check:", datetime.datetime.now())
        await check_player(id)
    update_state()
    await update_display()
    # print("End score check:", datetime.datetime.now())

@tasks.loop(minutes=1)
async def time_check():
    channel = bot.get_channel(config.announce_channel) # channel ID goes here
    await channel.send(state)
    # check for monday 5pm
    # remove beatmaps from state
    # announce results
    pass

@tasks.loop(hours=12)
async def reset_token():
    await apihelper.regen_token()
    # add in resetting usernames too


# commands

@bot.command(name="getrandom")
async def get_random(ctx: commands.Context, mode: str, *months: str):
    if ctx.author.id != config.nico_id:
        return

    good_bmss = await apihelper.get_good_sets(mode, months)
    random.shuffle(good_bmss)
    good_bmss = good_bmss[:4]
    message = format_bmsids(good_bmss)
    await ctx.channel.send(message)

@bot.command()
async def register(ctx: commands.Context, *, username: str):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) != 0:
        username = await apihelper.get_username(identity[0])
        await ctx.channel.send(
            f"This Discord account has already registered osu! account: {username}."
        )
        return

    rank, username, id = await apihelper.get_rank_username_id(username)
    if id in get_all_registered():
        await ctx.channel.send("You're already registered!")
        return

    player_data = PlayerData(
        discord_id=ctx.author.id,
        username=username,
        scores={bmsid: 0 for bmsid in state["beatmaps"]}
    )
    if rank < 50000:
        state["pros"][id] = player_data
    else:
        state["amateurs"][id] = player_data

    update_state()
    await update_display()
    await ctx.channel.send(f"Successfully registered {username}!")

@bot.command()
async def unregister(ctx: commands.Context):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) == 0:
        await ctx.channel.send("This Discord account has no registered osu! account.")
        return

    id = identity[0]
    username = await apihelper.get_username(id)

    if id in state["pros"]:
        state["pros"].pop(id)
    if id in state["amateurs"]:
        state["amateurs"].pop(id)
    update_state()
    await update_display()
    await ctx.channel.send(f"Successfully unregistered {username}!")

@bot.command(name="getrank")
async def get_rank(ctx: commands.Context, *, username: str):
    rank, username, _ = await apihelper.get_rank_username_id(username)
    await ctx.channel.send(f"{username} is rank {rank}.")

@bot.command()
async def identify(ctx: commands.Context):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) == 0:
        await ctx.channel.send("You're not registered!")
        return

    id = identity[0]
    username = await apihelper.get_username(id)
    await ctx.channel.send(f"Registered as {username}.")

@bot.command(name="start")
async def start(ctx: commands.Context, *map_ids: str):
    if ctx.author.id != config.nico_id:
        return

    # update rank

    if len(state["beatmaps"]) != 0: # tourney not running
        return

    blank_scores = {}
    for map_id in map_ids:
        blank_scores[map_id] = 0

    state["beatmaps"] = map_ids
    for player_data in (state["pros"] | state["amateurs"]).values():
        player_data["scores"] = blank_scores.copy()
    update_state()
    await update_display()

@bot.command(name="stop")
async def stop(ctx: commands.Context):
    if ctx.author.id != config.nico_id:
        return

    if len(state["beatmaps"]) == 0: # tourney runing
        return

    state["beatmaps"] = {}
    for player_data in (state["pros"] | state["amateurs"]).values():
        player_data["scores"] = {}
    update_state()
    await update_display()

@bot.command(name="manualcheck")
async def manual_check(ctx: commands.Context):
    if ctx.author.id != config.nico_id:
        return

    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) == 0:
        await ctx.channel.send("You're not registered!")
        return

    id = identity[0]
    await check_player(id)
    update_state()
    await update_display()


# helper

async def update_display():
    display_channel = bot.get_channel(config.display_channel)
    if display_channel.last_message_id == None:
        await display_channel.send("temp")
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
    message += format_bmsids(state["beatmaps"])

    message += "\n**PRO STANDINGS**\n"
    pro_scores = {}

    for pro_id, pro_data in state["pros"].items():
        name = pro_data["username"]
        pp = sum(pro_data["scores"].values())
        pro_scores[name] = pp
    for i, (pro_name, pro_pp) in enumerate(sorted(pro_scores.items(), key=lambda x: x[1], reverse=True)):
        message += f"{i+1}. {pro_name} ({pro_pp}pp)\n"

    message += "\n**AMATEUR STANDINGS**\n"

    amateur_scores = {}
    for amateur_id, amateur_data in state["amateurs"].items():
        name = amateur_data["username"]
        pp = sum(amateur_data["scores"].values())
        amateur_scores[name] = pp
    for i, (amateur_name, amateur_pp) in enumerate(sorted(amateur_scores.items(), key=lambda x: x[1], reverse=True)):
        message += f"{i+1}. {amateur_name} ({amateur_pp}pp)\n"

    await display_message.edit(content=message)

async def check_player(player_id):
    player_data = get_player_data_by_player_id(player_id)
    recent_scores = await apihelper.get_recent(player_id)
    recent_scores = [s for s in recent_scores if str(s["beatmap"]["beatmapset_id"]) in state["beatmaps"]]
    for recent_score in recent_scores:
        beatmapset_id = str(recent_score["beatmap"]["beatmapset_id"])
        if recent_score["pp"] == None:
            pp = 0
        else:
            pp = round(float(recent_score["pp"]))
        if player_data["scores"][beatmapset_id] < pp:
            channel = bot.get_channel(config.announce_channel)
            await channel.send(
                f"{recent_score['user']['username']} got {pp}pp " \
                f"on \"{recent_score['beatmap']['version']}\" difficulty " \
                f"of \"{recent_score['beatmapset']['title_unicode']}\"!"
            )
            player_data["scores"][beatmapset_id] = pp

def format_bmsids(bmsids):
    message = ""
    for bms in bmsids:
        message += f"<https://osu.ppy.sh/beatmapsets/{bms}>\n"
    return message

# state helpers

def get_all_registered():
    return list(state["pros"].keys()) + list(state["amateurs"].keys())

def get_player_by_discord_id(discord_id):
    return [k for (k, v) in (state["pros"] | state["amateurs"]).items() if v["discord_id"] == discord_id]

def get_player_data_by_player_id(player_id):
    return [v for (k, v) in (state["pros"] | state["amateurs"]).items() if k == player_id][0]

# saving/loading state

def update_state():
    write_file = open("state", "wb")
    pickle.dump(state, write_file)
    write_file.close()

if not os.path.isfile("state"):
    update_state()
else:
    with open("state", "rb") as f:
        state = pickle.load(f)


# bot init

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    score_check.start()
    # time_check.start()
    reset_token.start()

bot.run(config.bot_token)