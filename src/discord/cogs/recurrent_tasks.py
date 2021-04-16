from discord.ext import tasks
from discord.ext.commands import Cog

from .. import bot_config
from ...tournament.check_scores import check_player_scores
from ...tournament.tournament_state import TournamentState
from ...osu_api import api_helper
from ...utils import update_manager


class RecurrentTasks(Cog):
    instance = None

    def __init__(self, bot):
        self.bot = bot
        RecurrentTasks.instance = self

    @tasks.loop(minutes=1)
    async def score_check(self):
        state = TournamentState.instance

        # check that tournament is running
        if not state.is_running():
            await update_manager.update(self.bot)
            return

        state = TournamentState.instance

        for player_id in state.pros:
            await check_player_scores(player_id)
        for player_id in state.amateurs:
            await check_player_scores(player_id)
        await update_manager.update(self.bot)

    @tasks.loop(minutes=1)
    async def time_check(self):
        channel = self.bot.get_channel(bot_config.announce_channel())
        # await channel.send(state)
        # check for monday 5pm
        # remove beatmaps from state
        # announce results

    @tasks.loop(hours=12)
    async def reset_token(self):
        await api_helper.regen_token()
        # add in resetting usernames too


def get_recurrent_task_instance() -> RecurrentTasks:
    return RecurrentTasks.instance
