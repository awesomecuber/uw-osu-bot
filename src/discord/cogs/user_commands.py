from discord.ext.commands import Bot, Cog, command, Context

from ...osu_api import api_helper
from ...tournament import registration
from ...tournament.tournament_state import TournamentState
from ...utils import update_manager


class UserCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def register(self, ctx: Context, *, player_name: str):
        msg = await registration.register(ctx.author.id, player_name)
        await update_manager.update(self.bot)
        await ctx.channel.send(msg)

    @command()
    async def unregister(self, ctx: Context):
        msg = registration.unregister(ctx.author.id)
        await update_manager.update(self.bot)
        await ctx.channel.send(msg)

    @command(name="getrank")
    async def get_rank(self, ctx: Context, *, username: str):
        player = await api_helper.get_player_by_username(username)
        await ctx.channel.send(f"{username} is rank #{player.rank}.")

    @command()
    async def identify(self, ctx: Context):
        state = TournamentState.instance
        registered_person = state.get_person_by_discord_id(ctx.author.id)
        if registered_person is None:
            await ctx.channel.send("You're not registered!")
            return

        await ctx.channel.send(f"Registered as {registered_person.player.username}.")
