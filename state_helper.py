import asyncio, pickle

from uwosubot.tourney.person import Person
from uwosubot.tourney.tournament import Tournament
import uwosubot
from uwosubot.osu_api import api_helper

old_state = {'pros': {'6857375': {'discord_id': 156991104426704896, 'scores': {}, 'username': 'Beatrice'}, '4213009': {'discord_id': 315643073977778186, 'scores': {}, 'username': 'Cuber'}, '8816844': {'discord_id': 185612707993485312, 'scores': {}, 'username': 'omphen'}, '4753182': {'discord_id': 126182996968603648, 'scores': {}, 'username': 'YouBeDeadTwo'}, '2803422': {'discord_id': 211701525360279553, 'scores': {}, 'username': 'SupersonicSPX'}, '3794845': {'discord_id': 83061694347087872, 'scores': {}, 'username': 'Psych'}, '8083183': {'discord_id': 169587952777691136, 'scores': {}, 'username': 'rohasshiki'}, '5942615': {'discord_id': 92294966168014848, 'scores': {}, 'username': 'E n d'}}, 'amateurs': {'6981028': {'discord_id': 169660006814318595, 'scores': {}, 'username': 'BlackTea'}, '4551921': {'discord_id': 147945901955088384, 'scores': {}, 'username': 'Hakuyer'}, '11608068': {'discord_id': 328737826617425920, 'scores': {}, 'username': 'tjin7'}, '11405811': {'discord_id': 246042546537496576, 'scores': {}, 'username': 'Faranox'}, '5036976': {'discord_id': 134023487781076994, 'scores': {}, 'username': 'Prince\\_'}, '17113216': {'discord_id': 467577431767646218, 'scores': {}, 'username': 'colecrazy'}, '8455823': {'discord_id': 185574763303927808, 'scores': {}, 'username': 'Puhua'}, '10181936': {'discord_id': 134042798310686720, 'username': 'RShields', 'scores': {}}}, 'beatmaps': {}}

new_state: Tournament = uwosubot.tourney.tournament.Tournament()

async def main():
    for pro in old_state["pros"]:
        the_player = await api_helper.get_player_by_id(pro)
        the_person = Person(old_state["pros"][pro]["discord_id"], the_player)
        new_state.register(the_person)
    for amt in old_state["amateurs"]:
        the_player = await api_helper.get_player_by_id(amt)
        the_person = Person(old_state["amateurs"][amt]["discord_id"], the_player)
        new_state.register(the_person)

asyncio.run(main())
write_file = open("cur_state", "wb")
pickle.dump(new_state, write_file)
write_file.close()
print("a")
# new_state.register()
