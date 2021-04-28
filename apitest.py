import asyncio

from uwosubot.osu_api import api_helper

async def main():
    recent_plays = await api_helper.get_recent(8126553)
    print('a')

asyncio.run(main())
