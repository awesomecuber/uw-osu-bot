from discord.ext.commands import Bot, Cog, command, Context

from .. import state
from ..osu_api import api_helper
from ..tourney import check_scores, registration, test_valid_play
from ..utils import update_manager

# TODO: sanitize usernames in here
class UserCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def register(self, ctx: Context, *, player_name: str):
        msg = await registration.register(ctx.author.id, player_name)
        await ctx.channel.send(msg)
        await update_manager.update(self.bot)

    @command()
    async def unregister(self, ctx: Context):
        msg = registration.unregister(ctx.author.id)
        await ctx.channel.send(msg)
        await update_manager.update(self.bot)

    @command(name="getrank")
    async def get_rank(self, ctx: Context, *, username: str):
        player = await api_helper.get_player_by_username(username)
        await ctx.channel.send(f"{player.username} is rank #{player.rank}.")

    @command(name="getlastplay")
    async def get_last_play(self, ctx: Context):
        person = state.tournament.get_person_by_discord_id(ctx.author.id)
        recent_plays_json = await api_helper.get_recent(person.player.player_id)
        valid_plays_jsons = [play_json for play_json in recent_plays_json if test_valid_play.is_valid_play(play_json)]
        if len(valid_plays_jsons) == 0:
            await ctx.channel.send("You haven't set any valid plays recently!")
        else:
            last_play_json = valid_plays_jsons[0]
            await ctx.channel.send(embed=check_scores.get_embed(person, last_play_json))

    @command()
    async def identify(self, ctx: Context):
        registered_person = state.tournament.get_person_by_discord_id(ctx.author.id)
        if registered_person is None:
            await ctx.channel.send("You're not registered!")
            return

        await ctx.channel.send(f"Registered as {registered_person.player.username}.")
