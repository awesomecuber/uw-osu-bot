import os
import logging
import pickle
import random
import sys

from discord.ext import commands, tasks

from ..osu_api import api_helper
import bot_config
from ..tournament import manage_tournament, registration, tournament_save_handler, tournament_state
from ..utils import update_manager


logging.basicConfig(level=logging.INFO)


if "debug" in sys.argv:
    bot = commands.Bot(command_prefix="a!")
else:
    bot = commands.Bot(command_prefix="uw!")


# recurrent tasks
@tasks.loop(minutes=1)
async def score_check():
    # check that tournament is running
    if not tournament_state.is_running():
        await update_manager.update(bot)
        return

    # print("Start score check:", datetime.datetime.now())
    for id in state["pros"] | state["amateurs"]:
        await check_player(id)
    await update_manager.update(bot)


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
async def register(ctx: commands.Context, *, player_name: str):
    msg = registration.register(ctx.author.id, player_name)
    await update_manager.update(bot)
    await ctx.channel.send(msg)


@bot.command()
async def unregister(ctx: commands.Context):
    msg = registration.unregister(ctx.author.id)
    await update_manager.update(bot)
    await ctx.channel.send(msg)


@bot.command(name="getrank")
async def get_rank(ctx: commands.Context, *, username: str):
    player = await api_helper.get_player_by_username(username)
    await ctx.channel.send(f"{username} is rank #{player.rank}.")


@bot.command()
async def identify(ctx: commands.Context):
    registered_player = registration.get_player_by_discord_id(ctx.author.id)
    if registered_player is None:
        await ctx.channel.send("You're not registered!")
        return

    await ctx.channel.send(f"Registered as {registered_player.username}.")


# a set_code is the mapset id concatenated with the mod, like "294227NM"
@bot.command(name="start")
async def start(ctx: commands.Context, *set_codes: str):
    if ctx.author.id != bot_config.admin_id():
        return

    if not tournament_state.is_running():
        return

    manage_tournament.start_tournament()

    await update_manager.update(bot)


@bot.command(name="stop")
async def stop(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return

    if not tournament_state.is_running():
        return

    manage_tournament.stop_tournament()

    await update_manager.update(bot)


@bot.command(name="manualcheck")
async def manual_check(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return

    for id in state["pros"] | state["amateurs"]:
        # print(id, "score check:", datetime.datetime.now())
        await check_player(id)
    await update_manager.update(bot)


@bot.command(name="printstate")
async def print_state(ctx: commands.Context):
    if ctx.author.id != bot_config.admin_id():
        return
    print(tournament_state.get_state())


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


if not os.path.isfile("../../state"):
    await update_manager.update(bot)
else:
    tournament_save_handler.load_tournament()


# init
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
