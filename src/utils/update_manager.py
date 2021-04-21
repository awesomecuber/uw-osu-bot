from discord.ext.commands import Bot

from ..discord import update_displays
from ..tournament import tournament_save_handler


async def update(bot: Bot) -> None:
    tournament_save_handler.save_tournament_state()
    await update_displays.update_display(bot)
    await update_displays.update_detailed_display(bot)
