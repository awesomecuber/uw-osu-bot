from discord.ext import tasks
from discord.ext.commands import Bot, Cog
from .. import bot_config
from ...osu_api import api_helper
from ...tournament.tournament_state import TournamentState
from ...tournament.check_scores import check_player_scores
from ...utils import update_manager


class RecurrentTasks(Cog):
    instance = None

    def __init__(self, bot: Bot):
        self.bot = bot
        RecurrentTasks.instance = self

    @tasks.loop(minutes=1)
    async def score_check(self):

        state = TournamentState.instance

        # check that tournament is running
        if not state.is_running():
            await update_manager.update(self.bot)
            return

        for person in state.get_all_people():
            update_strings = await check_player_scores(person.player.player_id)
            for update_string in update_strings:
                await self._announce(update_string)

        await update_manager.update(self.bot)

    async def _announce(self, msg: str) -> None:
        channel = self.bot.get_channel(bot_config.announce_channel())
        await channel.send(msg)

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
