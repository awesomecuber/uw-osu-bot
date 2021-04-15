import copy
import os
import logging
import pickle
import random
import sys
from typing import TypedDict

import discord
from discord.errors import NotFound
from discord.ext import commands, tasks

from ..osu_api import api_helper
import bot_config


logging.basicConfig(level=logging.INFO)


# types
class ScoreData(TypedDict):
    pp: int
    sr: int


class PlayerData(TypedDict):
    discord_id: int
    username: str
    scores: dict[str, ScoreData]  # beatmapset_id to score


class BeatmapData(TypedDict):
    title: str
    mod: str


class State(TypedDict):
    pros: dict[str, PlayerData]  # user_id to data
    amateurs: dict[str, PlayerData]  # user_id to data
    beatmaps: dict[str, BeatmapData]  # beatmapset_ids to data


if "debug" in sys.argv:
    bot = commands.Bot(command_prefix="a!")
else:
    bot = commands.Bot(command_prefix="uw!")
state = State(pros={}, amateurs={}, beatmaps={})


# recurrent tasks
@tasks.loop(minutes=1)
async def score_check():
    # check that tournament is running
    if len(state["beatmaps"]) == 0:
        await update_display()
        await update_detailed_display()
        return

    # print("Start score check:", datetime.datetime.now())
    for id in state["pros"] | state["amateurs"]:
        await check_player(id)
    update_state()
    await update_display()
    await update_detailed_display()


@tasks.loop(minutes=1)
async def time_check():
    channel = bot.get_channel(bot_config.announce_channel()) # channel ID goes here
    await channel.send(state)
    # check for monday 5pm
    # remove beatmaps from state
    # announce results


@tasks.loop(hours=12)
async def reset_token():
    await api_helper.regen_token()
    # add in resetting usernames too


# commands
@bot.command(name="getrandom")
async def get_random(ctx: commands.Context, mode: str, months: list[str]):
    if ctx.author.id != bot_config.admin_id():
        return

    good_bmss = await api_helper.get_good_sets(mode, months)
    random.shuffle(good_bmss)
    good_bmss = good_bmss[:4]
    message = ""
    for bms in good_bmss:
        message += f"<https://osu.ppy.sh/beatmapsets/{bms}>\n"
    await ctx.channel.send(message)


@bot.command()
async def register(ctx: commands.Context, *, username: str):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) != 0:
        username = await api_helper.get_username(identity[0])
        await ctx.channel.send(
            f"This Discord account has already registered osu! account: {username}."
        )
        return

    rank, username, id = await api_helper.get_rank_username_id(username)
    if id in get_all_registered():
        await ctx.channel.send("You're already registered!")
        return

    player_data = PlayerData(
        discord_id=ctx.author.id,
        username=username,
        scores={bmsid: ScoreData(pp=0, sr=0) for bmsid in state["beatmaps"]}
    )
    if rank < 50000:
        state["pros"][id] = player_data
    else:
        state["amateurs"][id] = player_data

    update_state()
    await update_display()
    await update_detailed_display()
    await ctx.channel.send(f"Successfully registered {username}!")


@bot.command()
async def unregister(ctx: commands.Context):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) == 0:
        await ctx.channel.send("This Discord account has no registered osu! account.")
        return

    id = identity[0]
    username = await api_helper.get_username(id)

    if id in state["pros"]:
        state["pros"].pop(id)
    if id in state["amateurs"]:
        state["amateurs"].pop(id)
    update_state()
    await update_display()
    await update_detailed_display()
    await ctx.channel.send(f"Successfully unregistered {username}!")


@bot.command(name="getrank")
async def get_rank(ctx: commands.Context, *, username: str):
    rank, username, _ = await api_helper.get_rank_username_id(username)
    await ctx.channel.send(f"{username} is rank {rank}.")


@bot.command()
async def identify(ctx: commands.Context):
    identity = get_player_by_discord_id(ctx.author.id)
    if len(identity) == 0:
        await ctx.channel.send("You're not registered!")
        return

    id = identity[0]
    username = await api_helper.get_username(id)
    await ctx.channel.send(f"Registered as {username}.")


# a set_code is the mapset id concatenated with the mod, like "294227NM"
@bot.command(name="start")
async def start(ctx: commands.Context, *set_codes: str):
    if ctx.author.id != bot_config.admin_id():
        return

    # update rank

    if len(state["beatmaps"]) != 0: # tourney not running
        return

    beatmap_state = {}
    blank_scores = {}

    beatmap_names = await api_helper.get_beatmap_names(*[set_code[:-2] for set_code in set_codes])
    for set_code, map_name in zip(set_codes, beatmap_names):
        beatmap_state[set_code[:-2]] = BeatmapData(title=map_name, mod=set_code[-2:])
        blank_scores[set_code[:-2]] = ScoreData(pp=0, sr=0)

    state["beatmaps"] = beatmap_state
    for player_data in (state["pros"] | state["amateurs"]).values():
        player_data["scores"] = copy.deepcopy(blank_scores)
    update_state()
    await update_display()
    await update_detailed_display()


@bot.command(name="stop")
async def stop(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return

    if len(state["beatmaps"]) == 0: # tourney runing
        return

    state["beatmaps"] = {}
    for player_data in (state["pros"] | state["amateurs"]).values():
        player_data["scores"] = {}
    update_state()
    await update_display()
    await update_detailed_display()


@bot.command(name="manualcheck")
async def manual_check(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return

    for id in state["pros"] | state["amateurs"]:
        # print(id, "score check:", datetime.datetime.now())
        await check_player(id)
    update_state()
    await update_display()
    await update_detailed_display()


@bot.command(name="printstate")
async def print_state(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return
    print(state)


# helper
async def update_display():
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
    message += get_total_leaderboards(state["pros"])
    message += "\n**AMATEUR STANDINGS**\n"
    message += get_total_leaderboards(state["amateurs"])

    await display_message.edit(content=message)


def get_total_leaderboards(players):
    message = ""
    player_scores = get_player_scores(players)

    # v[1] is the regularized score, add those up for each map
    final_scores = {
        username: sum([v[1] for v in score_data.values()])
        for (username, score_data) in player_scores.items()
    } # map from username to total score
    for i, (username, total_score) in enumerate(sorted(final_scores.items(), key=lambda x: x[1], reverse=True)):
        message += f"{i+1}. {username} ({total_score:.1f})\n"
    return message


async def update_detailed_display():
    detail_channel: discord.TextChannel = bot.get_channel(bot_config.detail_channel())
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
    message_pros += get_map_leaderboards(state["pros"])
    message_ams = "------------------\n**AMATEURS**\n\n"
    message_ams += get_map_leaderboards(state["amateurs"])

    await discord_messages[1].edit(content=message_pros)
    await discord_messages[0].edit(content=message_ams)


def get_map_leaderboards(players):
    message = ""
    player_scores = get_player_scores(players)
    for mapset_id, mapset_data in state["beatmaps"].items():
        message += f"__{mapset_data['title']}__\n"

        for i, (username, score_data) in enumerate(
                    sorted(player_scores.items(), key=lambda x: x[1][mapset_id][0], reverse=True)
                ):
            score, normalized = score_data[mapset_id]
            message += f"{i+1}. {username}: {score:.1f} (normalized: {normalized:.1f})\n"
        message += "\n"
    return message


# this is probably needlessly long
# returns map from username to (map id to (score, normalized))
def get_player_scores(players):
    to_return = {}
    for player_data in players.values():
        scores = {}
        for map_id, score_data in player_data["scores"].items():
            scores[map_id] = calculate_score(score_data["pp"], score_data["sr"])
        to_return[player_data["username"]] = scores

    # add in normalized
    best_scores = {}
    for mapset_id in state["beatmaps"]:
        if len(to_return) == 0:
            best_score = 0
        else:
            best_score = max(v[mapset_id] for (_, v) in to_return.items())

        if best_score == 0:
            best_score = 1 # to prevent divide by zero
        best_scores[mapset_id] = best_score

    for player_name, player_data in to_return.items():
        for map_id, score in player_data.items():
            to_return[player_name][map_id] = (score, 250 * (score / best_scores[map_id]))
    return to_return


def is_valid_play(s):
    bmsid = str(s["beatmap"]["beatmapset_id"])

    if bmsid not in state["beatmaps"]:
        return False

    if s["pp"] is None:
        return False

    map_mod = state["beatmaps"][bmsid]["mod"]
    if map_mod == "NM":
        return len(s["mods"]) == 0
    elif map_mod == "HR":
        return len(s["mods"]) == 1 and s["mods"][0] == "HR"

    return True # shouldn't reach here


def calculate_score(pp, sr):
    return pp * sr**2


async def check_player(player_id):
    player_data = get_player_data_by_player_id(player_id)
    recent_scores = await api_helper.get_recent(player_id)
    recent_scores = [s for s in recent_scores if is_valid_play(s)]
    for recent_score in recent_scores:
        beatmapset_id = str(recent_score["beatmap"]["beatmapset_id"])
        pp = round(float(recent_score["pp"]))
        sr = recent_score["beatmap"]["difficulty_rating"]
        score = calculate_score(pp, sr)
        if calculate_score(**player_data["scores"][beatmapset_id]) < calculate_score(pp, sr):
            channel = bot.get_channel(bot_config.announce_channel())
            username = recent_score['user']['username']
            difficulty_name = recent_score['beatmap']['version']
            song_name = recent_score['beatmapset']['title_unicode']
            await channel.send(
                f"{username} got {pp}pp on \"{difficulty_name}\" difficulty ({sr}*) of \"{song_name}\"!"
                f" This results in a score of {score:.1f}."
            )
            player_data["scores"][beatmapset_id]["pp"] = pp
            player_data["scores"][beatmapset_id]["sr"] = sr


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

bot.run(bot_config.bot_token())
