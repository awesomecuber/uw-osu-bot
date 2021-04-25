import random

from discord.ext.commands import Bot, Cog, command, Context

from .. import bot_config, state
from ..osu_api.beatmapset import Beatmapset
from ..tourney import good_beatmapsets, manage_tournament
from ..utils import update_manager


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="getrandom")
    async def get_random(self, ctx: Context, mode: str, *months: str):
        if ctx.author.id != bot_config.admin_id():
            return

        good_bmss: list[Beatmapset] = await good_beatmapsets.get_good_beatmapsets(mode, months)
        random.shuffle(good_bmss)
        good_bmss = good_bmss[:4]

        message = ""
        for bms in good_bmss:
            message += f"<https://osu.ppy.sh/beatmapsets/{bms.beatmapset_id}>\n"
        await ctx.channel.send(message)

    # a set_code is the mapset id concatenated with the mod, like "294227NM"
    @command()
    async def start(self, ctx: Context, *set_codes: str):
        if ctx.author.id != bot_config.admin_id():
            return

        if state.tournament.is_running():
            return

        await manage_tournament.start_tournament(list(set_codes))
        print("starting tournament")
        await update_manager.update(self.bot)

    @command()
    async def stop(self, ctx: Context):
        if ctx.author.id != bot_config.admin_id():
            return

        if not state.tournament.is_running():
            return

        manage_tournament.stop_tournament()
        print("stopping tournament")
        await update_manager.update(self.bot)

    @command(name="manualcheck")
    async def manual_check(self, ctx: Context):
        if ctx.author.id != bot_config.admin_id():
            return

        from .recurrent_tasks import get_recurrent_task_instance
        get_recurrent_task_instance().score_check.restart()
