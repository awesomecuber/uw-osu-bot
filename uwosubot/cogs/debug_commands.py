from discord.ext.commands import Bot, Cog, command, Context

from .. import bot_config
from .. import state


class DebugCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="printstate")
    async def print_state(self, ctx: Context):
        if ctx.author.id != bot_config.admin_id():
            return
        print(state.tournament)
