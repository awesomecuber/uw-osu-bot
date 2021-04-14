import asyncio
import pickle

import apihelper

state = {'pros': {'6857375': {'discord_id': 156991104426704896, 'rank': 3286, 'scores': {'1341551': 312, '1308842': 151, '1329465': 248, '1125370': 100}}, '4213009': {'discord_id': 315643073977778186, 'rank': 30471, 'scores': {'1341551': 129, '1308842': 107, '1329465': 176, '1125370': 69}}, '8816844': {'discord_id': 185612707993485312, 'rank': 1508, 'scores': {'1341551': 360, '1308842': 301, '1329465': 369, '1125370': 214}}, '4753182': {'discord_id': 126182996968603648, 'rank': 13079, 'scores': {'1341551': 0, '1308842': 0, '1329465': 187, '1125370': 155}}, '2803422': {'discord_id': 211701525360279553, 'rank': 10775, 'scores': {'1341551': 316, '1308842': 158, '1329465': 239, '1125370': 146}}, '3794845': {'discord_id': 83061694347087872, 'rank': 30924, 'scores': {'1341551': 116, '1308842': 73, '1329465': 136, '1125370': 34}}, '8083183': {'discord_id': 169587952777691136, 'rank': 47056, 'scores': {'1341551': 219, '1308842': 24, '1329465': 188, '1125370': 33}}, '5942615': {'discord_id': 92294966168014848, 'rank': 5823, 'scores': {'1341551': 280, '1308842': 0, '1329465': 0, '1125370': 0}}}, 'amateurs': {'6981028': {'discord_id': 169660006814318595, 'rank': 170730, 'scores': {'1341551': 85, '1308842': 29, '1329465': 149, '1125370': 35}}, '4551921': {'discord_id': 147945901955088384, 'rank': 56928, 'scores': {'1341551': 85, '1308842': 18, '1329465': 156, '1125370': 36}}, '11608068': {'discord_id': 328737826617425920, 'rank': 164160, 'scores': {'1341551': 28, '1308842': 0, '1329465': 65, '1125370': 30}}, '11405811': {'discord_id': 246042546537496576, 'rank': 195103, 'scores': {'1341551': 75, '1308842': 2, '1329465': 47, '1125370': 0}}, '5036976': {'discord_id': 134023487781076994, 'rank': 54137, 'scores': {'1341551': 201, '1308842': 47, '1329465': 176, '1125370': 14}}, '17113216': {'discord_id': 467577431767646218, 'rank': 88091, 'scores': {'1341551': 49, '1308842': 14, '1329465': 116, '1125370': 0}}, '8455823': {'discord_id': 185574763303927808, 'rank': 258004, 'scores': {'1341551': 31, '1308842': 13, '1329465': 51, '1125370': 0}}}, 'beatmaps': ('1341551', '1308842', '1329465', '1125370')}

async def update(users):
    for user_id in users:
        del users[user_id]["rank"]
        users[user_id]["username"] = await apihelper.get_username(user_id)

asyncio.run(update(state["pros"]))
asyncio.run(update(state["amateurs"]))

write_file = open("state", "wb")
pickle.dump(state, write_file)
write_file.close()
