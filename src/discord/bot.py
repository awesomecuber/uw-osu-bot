import os
import logging
import sys

from discord.ext import commands

from . import bot_config
from ..tournament import tournament_save_handler
from ..utils import update_manager

from .cogs.admin_commands import AdminCommands
from .cogs.debug_commands import DebugCommands
from .cogs.recurrent_tasks import RecurrentTasks, get_recurrent_task_instance
from .cogs.user_commands import UserCommands

logging.basicConfig(level=logging.INFO)

if "debug" in sys.argv:
    bot = commands.Bot(command_prefix="a!")
else:
    bot = commands.Bot(command_prefix="uw!")

bot.add_cog(AdminCommands(bot))
bot.add_cog(DebugCommands(bot))
bot.add_cog(RecurrentTasks(bot))
bot.add_cog(UserCommands(bot))


# init
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    get_recurrent_task_instance().score_check.start()
    get_recurrent_task_instance().reset_token.start()

    # Initialization
    if not os.path.isfile("../../state"):
        await update_manager.update(bot)
    else:
        tournament_save_handler.load_tournament()


bot.run(bot_config.bot_token())
