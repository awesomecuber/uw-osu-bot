from discord.ext.commands import Bot

from .. import update_displays
from .. import state_save_handler


async def update(bot: Bot) -> None:
    state_save_handler.save_tournament_state()
    await update_displays.update_display(bot)
    await update_displays.update_detailed_display(bot)
