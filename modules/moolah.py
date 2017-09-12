import discord
import random
import logging
from modules.sqdatabase import*
logger = logging.getLogger(__name__)

def givemoolah(serverlist):
    logging.info("Giving Moolah!")
    for server in serverlist:
        for member in server.members:
            if member.voice_channel != None and member.voice_channel.id !=server.afk_channel.id:
                Vid =  member.voice_channel.id  
                test = discord.utils.get(server.channels, id=Vid)
                if len(test.voice_members) > 1:
                    number = 100
                    memberz = member
                    if member.bot != True:
                        if memberz != None and memberz.self_deaf != True:
                            red = database(serverid =server.id,id=memberz.id)
                            red.update(number,arg="coin",types="+")
                        elif memberz.self_mute == True and memberz.self_deaf != True:
                            muteno = 75
                            red = database(serverid =server.id,id=memberz.id)
                            red.update(muteno,arg="coin",types="+")
                        elif memberz.self_deaf == True:
                            muteno = 75
                            red = database(serverid =server.id,id=memberz.id)
                            red.update(muteno,arg="coin",types="+")
    logging.info("Finished Giving Moolah")
