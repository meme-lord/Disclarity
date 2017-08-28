import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import time
import discord
import json
import logging
import os
from random import randint
from random import choice as randchoice
try:
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False
import aiohttp
import http
import praw #reddit posting
import sys #system
import urllib #view websites
import time #get time
import signal
import numpy as np
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import sqlite3
from prettytable import PrettyTable
from difflib import get_close_matches



Client = discord.Client()
bot_prefix= "."
client = commands.Bot(command_prefix=bot_prefix)

secure_random = random.SystemRandom()

#################################STORAGE#################################
DROPAPI = os.environ['DROPBOXAPI']
dbx = dropbox.Dropbox(DROPAPI)
LOCALFILE = 'USER.db'
BACKUPPATH = '/USER.db'

def file_len(fname):
    with open(fname,encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def backup():
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_delete(BACKUPPATH)
            dbx.files_upload(f.read(), BACKUPPATH, mode=dropbox.files.WriteMode.overwrite)
            print("Uploaded!")
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


def userlist():
##format##
    listusers = client.get_all_members()
    #print("Saving List of Users")
    with open('Users.txt', 'w',encoding='utf-8') as f:
        for x in listusers:
            f.write(str(x.name)+"\n")
            ID2 = int(x.id)
            NAME2 = str(x.name)
            NICK2 = str(x.nick)
            ROLE2 = str(x.top_role)
            COIN = int(0)
            try:
                conn.execute("INSERT INTO SERVER VALUES (?, ?, ?, ?, ?);", (ID2, NAME2, NICK2, ROLE2, COIN))
            except sqlite3.IntegrityError :
                pass
    cursor = conn.execute("SELECT ID, NAME, NICK, COIN from SERVER")
    #for row in cursor:
    #    print( "ID = ", row[0])
    #    print ("NAME = ", row[1].encode('utf-8'))
    #    print ("NICK = ", row[2].encode('utf-8'))
    #    print( "COIN = ", row[3], "\n")

    print("User Count:"+str(file_len('Users.txt')))


def restore():
    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    try:
        try:
            os.remove(LOCALFILE)
            print("USER.db Detected Removing.....Done")
        except OSError:
            pass
        print("Downloading current " + BACKUPPATH + " from Dropbox, overwriting " + LOCALFILE + "...")
        dbx.files_download_to_file(LOCALFILE, BACKUPPATH)
    except:
        print("RESTORE FAILED NO DATABASE!!")
        print("Ignoring and continuing ..")
        pass
#############################################################################
def signal_handler(signum, frame):
    raise Exception("Timed out!")

###################################################################USER LOG AND DATA UPLOAD###############################
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
restore()
global conn
conn = sqlite3.connect('USER.db') 
##########################################################################################################################

@client.event
async def on_ready():
    print("____________________________________")
    print("{} Is Now Online!".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=discord.Game(name='Doing what needs to be Done!'))
    userlist()
    print("____________________________________")
    while True:
        print("Giving Moolah !")
        memberss = client.get_server("205438531429072897").members
        for no in memberss:
            if no.voice_channel != None and no.voice_channel.id !="216282244665311232":
                Vid =  no.voice_channel.id   
                test = discord.utils.get(client.get_server("205438531429072897").channels, id=Vid)
                if len(test.voice_members) > 1:
                    #print ("Opened database successfully")
                    number = 100
                    memberz = no
                    global conn
                    if no.id != "341326594113011712" :
                        if memberz != None and memberz.self_deaf != True:
                            conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (number, memberz.id)) 
                            #print("Coin added")
                        elif memberz.self_mute == True and memberz.self_deaf != True:
                        	muteno = 75
                        	conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (muteno, memberz.id)) 
                        elif memberz.self_deaf == True:
                        	muteno = 25
                        	conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (muteno, memberz.id)) 
        print("Finished Giving Moolah")
        #############TEST AUTO BACKUP####################
        conn.commit() 
        conn.close()
        backup()
        conn = sqlite3.connect('USER.db')
        await asyncio.sleep(1800)




mainchannel= '205438531429072897'
###################################FAREWELL###################################
@client.event
async def on_member_remove(member):
    embed=discord.Embed(title="                   ", description="Let us bid "+member.display_name+" a grand farewell from our humble abode! :wave: ", color=0xf1ec1b)
    await client.send_message(client.get_channel(mainchannel), embed=embed)



###################################WELCOME###################################
@client.event
async def on_member_join(member):
    x = random.randrange(0,13)
    if(x==0):
        await client.send_message(client.get_channel(mainchannel), "http://www.relatably.com/m/img/welcome-memes/63341322.jpg")
    if(x==1):
        await client.send_message(client.get_channel(mainchannel), "http://memeshappen.com/media/created/2017/03/I-dont-always-welcome-people-to-the-team-But-when-I-do-I-welcome-YOU.jpg")
    if(x==2):
        await client.send_message(client.get_channel(mainchannel), "https://ci.memecdn.com/5150905.jpg")
    if(x==3):
        await client.send_message(client.get_channel(mainchannel), "https://cdn.meme.am/cache/instances/folder407/66962407.jpg")
    if(x==4):
        await client.send_message(client.get_channel(mainchannel), "https://cdn.meme.am/cache/instances/folder326/500x/67462326.jpg")
    if(x==5):
        await client.send_message(client.get_channel(mainchannel), "http://slodive.com/wp-content/uploads/2017/04/W1-1.jpg")
    if(x==6):
        await client.send_message(client.get_channel(mainchannel), "https://s-media-cache-ak0.pinimg.com/originals/57/22/1d/57221d1e3f6e3b0c7a1e2ead4bb364a0.jpg")
    if(x==7):
        await client.send_message(client.get_channel(mainchannel), "https://sd.keepcalm-o-matic.co.uk/i-w600/welcome-to-the-crew-2.jpg")
    if(x==8):
        await client.send_message(client.get_channel(mainchannel), "https://cdn.meme.am/instances/55058017.jpg")
    if(x==9):
        await client.send_message(client.get_channel(mainchannel), "http://www.relatably.com/m/img/welcome-memes/2e0ea24cef3313b41cc0da552fa04b5120ac1eb08b737dbf2691cd7c826b0ae5.jpg")
    if(x==10):
        await client.send_message(client.get_channel(mainchannel), "https://i.imgflip.com/a6wrw.jpg")
    if(x==11):
        await client.send_message(client.get_channel(mainchannel), "http://memeshappen.com/media/created/Welcome-I39m-glad-you-are-here-meme-27690.jpg")
    if(x==12):
        await client.send_message(client.get_channel(mainchannel), "https://cdn.meme.am/cache/instances/folder454/500x/74797454/mr-burns-meme-welcome-aboard-now-get-to-work.jpg")
    if(x==13):
        await client.send_message(client.get_channel(mainchannel), "https://i.imgflip.com/jt3h8.jpg")
    embed=discord.Embed(title="                   ", description="Welcome to our humble abode :island:  "+member.mention, color=0xf1ec1b)
    await client.send_message(client.get_channel(mainchannel), embed=embed)
    #setting Role
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Recruit")
    print("Setting Role :"+str(role.name)+" Name: "+str(member.name))
    await client.add_roles(member, role)
    if not member.name in open('Users.txt', encoding='utf-8').read():
        open('Users.txt','w', encoding='utf-8').write(member.name)





###################################NICKNAME lockdown###################################
@client.event		
async def on_member_update(before, after):
    if "341326594113011712" in str(after.id):
        if not(before.nick == "Fiddling Bot"):
            await client.change_nickname(after, "Fiddling Bot")
            print("Reverted Music bots Nickname to Fiddling Bot")
    #if "138684247853498369" in str(after.id):
    #    if not(after.nick == "Xelor"):
    #        await client.change_nickname(after, "Xelor")
    #        print("Reverted Xelor Nickname to Xelor")
    if "341694509744128001" in str(after.id):
        if not(after.nick == "Innocent Bot"):
            await client.change_nickname(after, "Innocent Bot")
            print("Reverted Innocent Bot Nickname to Innocent Bot")

    ###################################BOT AUTO DISCONNECT FEATURE###################################
    bot = discord.utils.get(client.get_server("205438531429072897").members, nick="Fiddling Bot")
    if bot != None:
        if bot.voice.voice_channel == None:
            pass
        else:
            Vid =  bot.voice.voice_channel.id   
            test = discord.utils.get(client.get_server("205438531429072897").channels, id=Vid)
            if len(test.voice_members) < 2:
                botkickm = await client.send_message(client.get_channel("272821211468136451"), "Kick That Bot Out!")
                botkickm1= await client.send_message(client.get_channel("272821211468136451"), "!disconnect")
                await asyncio.sleep(1.2)
                await client.delete_message(botkickm)
                await client.delete_message(botkickm1)
    ###################################ROLES LOCKDOWN###################################
    try:
        if "160411092617527306" in str(after.id):
            if not "Mod" in str(after.roles):
                await client.replace_roles(after, (discord.utils.get(client.get_server("205438531429072897").roles, name="Mod")))
    except AttributeError:
        pass
    ##############################DATABASE UPDATE##########################################################################################
    playernameb = before.name
    playernamea = after.name
    playernickb = before.nick
    playernicka = after.nick
    if playernameb != playernamea:
        conn.execute("UPDATE SERVER SET NAME = ? WHERE ID=?", (after.name, after.id)) 
    if playernickb != playernicka:
        conn.execute("UPDATE SERVER SET NICK = ? WHERE ID=?", (after.nick, after.id))
    #######################################################################################################################################
            
#command1
@client.command(pass_context = True)
async def getbans(ctx):
    """Get the List of Currently Banned People"""
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of Banned Members", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context = True)
async def clear(ctx, number):
    """Clears messages that are less than 14 days old"""
    mgs = [] #Empty list to put all the messages in the log FOR 14 DAYS OR BELOW
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)
    
@client.command(pass_context = True)
async def clearO(ctx, number):
    """Clears messages that are more than 14 days old(slow)"""
    number = int(number) #Converting the amount of messages to delete to an integer
    counter = 0
    async for x in client.logs_from(ctx.message.channel, limit = number):
        if counter < number:
            await client.delete_message(x)
            counter += 1
            await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even

@client.command(pass_context=True)
async def echo(ctx, *, echo: str):
    """The Bot follows your lead!"""
    await client.delete_message(ctx.message)
    await client.say(echo)
    
@client.command(pass_context=True)
async def kill(ctx, *, member : discord.Member = None):
    """Kills the Given Target (kick)"""
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Primus")
    memroles = ctx.message.author.roles
    if role in memroles:
        await client.delete_message(ctx.message)
        if (member is None):
            await client.say("I can't Kill Someone unless you tell me who to kill!")
            return
        elif (member.id == "138684247853498369"):
            await client.say("Ya Can't Touch me Bruh, get on my Level! :sunglasses:")
            print("yolo")
        elif (member.id == "341694509744128001"):
            await client.say("Why do you want to kill me ! I am an innocent bot!.")
        else:
            await client.say(str(member.display_name)+" Has mysteriously gone missing , the Police suspect Kira..eheh")
            await client.kick(member)
    else:
        await client.delete_message(ctx.message)
        await client.say("Sorry My man !, you dont have the permissions...*the cops are on to you*")


		
@client.command(pass_context = True)
async def poll(context):
	message = context.message
	   

	# multiple lines
	if len(message.content.split('\n')) > 1:
		await multi_poll(message)
	else:
		# yes, no, shrug
		# TODO make these customizable, as some people prefer
		# :squid: to :shrug:
		for reaction in ('👍', '👎'):
			await client.add_reaction(message, reaction)
	"""Takes a Poll eg. .poll Red or Blue ."""
	# no matter what, not knowing is always an option
	await client.add_reaction(message, '🤷')

	

async def multi_poll(message):	
	# the first line is the command line.
	# ignore the first line
	for line in message.content.split('\n')[1:]:
		if 'A:' in line:
			await client.add_reaction(message, ':A_:342002935783489536')
		if 'B:' in line:
			await client.add_reaction(message, ':B_:342002993115168768')
		if 'C:' in line:
			await client.add_reaction(message, ':C_:342002993123557396')
		if 'D:' in line:
			await client.add_reaction(message, ':D_:342002992993796097')
		if 'E:' in line:
			await client.add_reaction(message, ':E_:342002993199054849')





@client.event
async def on_message(message):
    await client.process_commands(message)
    authorr = message.author
    contents = message.content
    print("Name: [{}]".format(authorr.name)+" Nickname: [{}]".format(authorr.nick)+" ID: [{}]".format(authorr.id)+" String Length:"+str(len(message.content)))
    number = 0
    if not "." in message.content[0:1] and not "!" in message.content[0:1] :
        if authorr != None and authorr.id != "341694509744128001":
            conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (number, authorr.id)) 

    if authorr.name != "Innocent Bot":
        if len(message.content) > 850 :
            await client.delete_message(message)
            warningmsg1 = await client.send_message(message.channel, "Sorry Buddy you have crossed the Character Limit(1000) around these parts! :sunglasses:")
            warningmsg2 = await client.send_message(message.channel, "If u have any Complaints take it to Hawkens™,or the Suggestion Box \n You know what , take all the Complaints to Hawkens™ :joy: ")
            await asyncio.sleep(2)
            await client.delete_message(warningmsg1)
            await client.delete_message(warningmsg2)




@client.command(aliases=['lovecalc'])
async def lovecalculator( lovers: discord.Member, loved: discord.Member):
    """Calculate the love percentage!"""
    x = lovers.display_name
    y = loved.display_name
    url = 'https://www.lovecalculator.com/love.php?name1={}&name2={}'.format(x.replace(" ", "+"), y.replace(" ", "+"))
    async with aiohttp.ClientSession() as session:
    	async with session.get(url) as response:
    		soupObject = BeautifulSoup(await response.text(), "html.parser")
    		try:
    			description = soupObject.find('div', attrs={'class': 'result score'}).get_text().strip()
    		except:
    			description = 'Dr. Love is busy right now'

    try:
        z = description[:2]
        z = int(z)
        if z > 50:
            emoji = '❤'
        else:
            emoji = '💔'
        title = 'Dr. Love says that the love percentage for {} and {} is:'.format(x, y)
    except:
        emoji = ''
        title = 'Dr. Love has left a note for you.'
            
    description = emoji + ' ' + description + ' ' + emoji
    em = discord.Embed(title=title, description=description, color=discord.Color.red())
    await client.say(embed=em)


@client.command(pass_context=True)
async def insult(ctx,user: discord.Member):
    """Insults The specified User (HARSH ROASTS)"""
    def _read_json():
        with open('data/insult/insults.json', encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data
    insults =_read_json()
    x1 = user.id
    msg = ' '
    if user != None:
        if user.display_name == "Innocent Bot":
            user = ctx.message.author
            msg = " How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
            await client.say(user.mention + msg)
        else:
            #await client.delete_message(ctx.message)
            await client.say(user.mention + msg + randchoice(insults))
    else:
        #await client.delete_message(ctx.message)
        await client.say(ctx.message.author.mention + msg + randchoice(insults))



@client.command(pass_context=True)
async def RPS(ctx,player2: discord.Member):
    """The Great Game of Rock Paper Sizzors!"""
    player1 = ctx.message.author
    await client.say("Lets the Grand Game of Rock Paper Sizzers BEGIN!")
    await asyncio.sleep(2)
    await client.say("After I finish Making it :joy: ")

    



class InvalidFileIO(Exception):
    pass

class DataIO():
    def __init__(self):
        self.logger = logging.getLogger("red")

    def save_json(self, filename, data):
        """Atomically saves json file"""
        rnd = randint(1000, 9999)
        path, ext = os.path.splitext(filename)
        tmp_file = "{}-{}.tmp".format(path, rnd)
        self._save_json(tmp_file, data)
        try:
            self._read_json(tmp_file)
        except json.decoder.JSONDecodeError:
            self.logger.exception("Attempted to write file {} but JSON "
                                  "integrity check on tmp file has failed. "
                                  "The original file is unaltered."
                                  "".format(filename))
            return False
        os.replace(tmp_file, filename)
        return True

    def load_json(self, filename):
        """Loads json file"""
        return self._read_json(filename)

    def is_valid_json(self, filename):
        """Verifies if json file exists / is readable"""
        try:
            self._read_json(filename)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False

    def _read_json(self, filename):
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data

    def _save_json(self, filename, data):
        with open(filename, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4,sort_keys=True,
                separators=(',',' : '))
        return data

    def _legacy_fileio(self, filename, IO, data=None):
        """Old fileIO provided for backwards compatibility"""
        if IO == "save" and data != None:
            return self.save_json(filename, data)
        elif IO == "load" and data == None:
            return self.load_json(filename)
        elif IO == "check" and data == None:
            return self.is_valid_json(filename)
        else:
            raise InvalidFileIO("FileIO was called with invalid"
                " parameters")

def get_value(filename, key):
    with open(filename, encoding='utf-8', mode="r") as f:
        data = json.load(f)
    return data[key]

def set_value(filename, key, value):
    data = fileIO(filename, "load")
    data[key] = value
    fileIO(filename, "save", data)
    return True

dataIO = DataIO()
fileIO = dataIO._legacy_fileio # backwards compatibility


API_URL = "https://www.cleverbot.com/getreply?"


class CleverbotError(Exception):
    pass

class NoCredentials(CleverbotError):
    pass

class InvalidCredentials(CleverbotError):
    pass

class APIError(CleverbotError):
    pass

class OutOfRequests(CleverbotError):
    pass

class OutdatedCredentials(CleverbotError):
    pass



settings = dataIO.load_json("data/cleverbot/settings.json")
instances = {}

@client.group(no_pm=True, invoke_without_command=True, pass_context=True)
async def c(ctx, *, message):
    """Talk With me ! , Have a Nice Conversation!"""
    author = ctx.message.author
    channel = ctx.message.channel
    try:
        result = await get_response(author, message)
    except NoCredentials:
        await client.send_message(channel, "The owner needs to set the credentials first.\n"
                                                 "See: `[p]cleverbot apikey`")
    except APIError:
        await client.send_message(channel, "Error contacting the API.")
    except InvalidCredentials:
        await client.send_message(channel, "The token that has been set is not valid.\n"
                                                 "See: `[p]cleverbot apikey`")
    except OutOfRequests:
        await client.send_message(channel, "You have ran out of requests for this month. "
                                                 "The free tier has a 5000 requests a month limit.")
    except OutdatedCredentials:
        await client.send_message(channel, "You need a valid client.com api key for this to "
                                                 "work. The old client.io service will soon be no "
                                                 "longer active. See `[p]help cleverbot apikey`")
    else:
        await client.say(result)

#@client.command()
#async def toggle():
#    """Toggles reply on mention"""
#    settings["TOGGLE"] = not settings["TOGGLE"]
#    if settings["TOGGLE"]:
#        await client.say("I will reply on mention.")
#    else:
#        await client.say("I won't reply on mention anymore.")
#   dataIO.save_json("data/cleverbot/settings.json", settings)

#@client.command()
#async def apikey(key: str):
#    """Sets token to be used with client.com
#
#    You can get it from https://www.client.com/api/
#    Use this command in direct message to keep your
#    token secret"""
#    settings["cleverbot_key"] = key
#    settings.pop("key", None)
#    settings.pop("user", None)
#    dataIO.save_json("data/cleverbot/settings.json", settings)
#    await client.say("Credentials set.")

async def get_response(author, text):
    payload = {}
    payload["key"] = get_credentials()
    payload["cs"] = instances.get(author.id, "")
    payload["input"] = text
    session = aiohttp.ClientSession()

    async with session.get(API_URL, params=payload) as r:
        if r.status == 200:
            data = await r.text()
            data = json.loads(data, strict=False)
            instances[author.id] = data["cs"] # Preserves conversation status
        elif r.status == 401:
            raise InvalidCredentials()
        elif r.status == 503:
            raise OutOfRequests()
        else:
            raise APIError()
    await session.close()
    return data["output"]

def get_credentials():
    if "cleverbot_key" not in settings:
        if "key" in settings:
            raise OutdatedCredentials() # old client.io credentials
    try:
        return settings["cleverbot_key"]
    except KeyError:
        raise NoCredentials()

async def on_message(message):
    if not settings["TOGGLE"] or message.server is None:
        return

    if not client.user_allowed(message):
        return

    author = message.author
    channel = message.channel

    if message.author.id != client.user.id:
        to_strip = "@" + author.server.me.display_name + " "
        text = message.clean_content
        if not text.startswith(to_strip):
            return
        text = text.replace(to_strip, "", 1)
        await client.send_typing(channel)
        try:
            response = await client.get_response(author, text)
        except NoCredentials:
            await client.send_message(channel, "The owner needs to set the credentials first.\n"
                                                     "See: `[p]cleverbot apikey`")
        except APIError:
            await client.send_message(channel, "Error contacting the API.")
        except InvalidCredentials:
            await client.send_message(channel, "The token that has been set is not valid.\n"
                                                     "See: `[p]cleverbot apikey`")
        except OutOfRequests:
            await client.send_message(channel, "You have ran out of requests for this month. "
                                                     "The free tier has a 5000 requests a month limit.")
        except OutdatedCredentials:
            await client.send_message(channel, "You need a valid client.com api key for this to "
                                                     "work. The old client.io service will soon be no "
                                                     "longer active. See `[p]help cleverbot apikey`")
        else:
            await client.send_message(channel, response)

def check_folders():
    if not os.path.exists("data/cleverbot"):
        print("Creating data/cleverbot folder...")
        os.makedirs("data/cleverbot")


def check_files():
    f = "data/cleverbot/settings.json"
    data = {"TOGGLE" : True}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)


def unic(msg): #convert text for saving in .txt
    return msg.encode("utf-8")



@client.command(pass_context = True)
async def meme(ctx):
    """Get Your Daily Dose of Memes"""
    with open("list.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content] 
        channel1 = "341721336743329793"
        #await client.delete_message(ctx.message)
        comment =  await client.say(secure_random.choice(content))




#@client.command(pass_context = True)
#async def test():





    ###########################################################################################
    """bot = discord.utils.get(client.get_server("205438531429072897").members, nick="Fiddling Bot")
    try:
        if bot.voice.voice_channel != None:
            Vid =  bot.voice.voice_channel.id
            test = discord.utils.get(client.get_server("205438531429072897").channels, id=Vid)
            if len(test.voice_members) < 2:
                await client.say("Kick That bot out!")
                await client.send_message(client.get_channel("272821211468136451"), "!disconnect")
            else:
                messages = await client.say("The bot can stay")
                await asyncio.sleep(3)
                await client.delete_message(messages)
    except AttributeError:
        messages = await client.say("The Music Bot isnt in a Channel Mate")
        await asyncio.sleep(3)
        await client.delete_message(messages)"""


@client.command(pass_context = True)
async def nickchange(ctx,member, nickname):
    """Changes Nickname of the user!"""
    if discord.utils.get(ctx.message.author.roles, name="Primus"):
        print("Allowed!")
        memberz = discord.utils.get(client.get_server("205438531429072897").members, nick=member)
        if memberz != None :
            await client.change_nickname(memberz, nickname)
            await client.delete_message(ctx.message)
        else:
            if member.isdigit():
                    memberzz = discord.utils.get(client.get_server("205438531429072897").members, id=member)
                    print(memberzz.nick)
                    if memberzz != None :
                        await client.change_nickname(memberz, nickname)
                        await client.delete_message(ctx.message)
    else:
        print("Not Allowed"+member.name)


@client.command(pass_context = True)
async def shutdown(ctx):
    """SAVES ALL USER DATA and turns off the bot/restart"""
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Primus")
    memroles = ctx.message.author.roles
    if role in memroles:
        print("Saving Files to Dropbox")
        conn.commit() 
        conn.close()
        backup()
        warning = await client.say("Saving Data Files....")
        await asyncio.sleep(1.2)
        warning2 = await client.say("Shutting Down....")
        await asyncio.sleep(1.2)
        await client.delete_message(warning)
        await client.delete_message(warning2)
        await asyncio.sleep(1.2)
        await client.logout()
        sys.exit()
    else:
        warning3 = await client.say("You Dont Have the Permissions Mate")
        await asyncio.sleep(1.2)
        await client.delete_message(warning3) 

@client.command(pass_context = True)
async def addcoin(ctx,member,number):
    """Gives Moolah to specified user Ultra Admin use only"""
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Primus")
    memroles = ctx.message.author.roles
    if role in memroles:
        print ("Opened database successfully")
        memberz = discord.utils.get(client.get_server("205438531429072897").members, name=member)
        if memberz != None:
            conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (number, memberz.id)) 
            await client.say("No.of Moolah Added: "+str(number))
        else:
            members = discord.utils.get(client.get_server("205438531429072897").members, nick=member)
            if members != None:
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (number, members.id)) 
                await client.say("No.of Moolah Added: "+str(number))

@client.command(pass_context = True)
async def removecoin(ctx,member,number):
    """Gives Moolah to specified user Ultra Admin use only"""
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Primus")
    memroles = ctx.message.author.roles
    if role in memroles:
        print ("Opened database successfully")
        memberz = discord.utils.get(client.get_server("205438531429072897").members, name=member)
        if memberz != None:
            conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=?", (number, memberz.id)) 
            await client.say("No.of Moolah Removed: "+str(number))
        else:
            members = discord.utils.get(client.get_server("205438531429072897").members, nick=member)
            if members != None:
                conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=?", (number, members.id)) 
                await client.say("No.of Moolah Removed: "+str(number))


@client.command(pass_context = True)
async def userinfo(ctx,member):
    """Gets User Info"""
    memberz = search(ctx,member)
    #memberz = discord.utils.get(client.get_server("205438531429072897").members, name=member)
    if memberz != None:
        cursor = conn.execute("SELECT NAME, NICK, ID,COIN FROM SERVER WHERE ID=:Id", {"Id": memberz.id})
        for row in cursor:
            idz = row[0]
            namez =  row[1]
            nickz =  row[2]
            coin = row[3]
            embed=discord.Embed(title="User Information", description="Name: "+str(idz)+"\n"+"Nickname: "+str(namez)+"\n"+"ID: "+str(nickz)+"\n"+"Moolah: "+str(coin), color=0xf1ec1b)
            await client.say(embed=embed)
    else:
        memberz = discord.utils.get(client.get_server("205438531429072897").members, nick=member)
        if memberz != None:
            cursor = conn.execute("SELECT NAME, NICK, ID,COIN FROM SERVER WHERE ID=:Id", {"Id": memberz.id})
            for row in cursor:
                idz = row[0]
                namez =  row[1]
                nickz =  row[2]
                coin = row[3]
                embed=discord.Embed(title="User Information", description="Name: "+str(idz)+"\n"+"Nickname: "+str(namez)+"\n"+"ID: "+str(nickz)+"\n"+"Moolah: "+str(coin), color=0xf1ec1b)
                await client.say(embed=embed)


@client.command(pass_context = True)
async def topdog():
    cursor = conn.execute(" SELECT NAME, COIN FROM SERVER ORDER BY COIN DESC LIMIT 10")
    List1 = []
    List2 = []
    for row in cursor:
        Name = row[0]
        coin = row[1]
        List1.append(Name)
        List2.append(coin)
    x = PrettyTable()
    x.field_names = ["Names","Moolah"]
    x.add_row([List1[0],List2[0]])
    x.add_row([List1[1],List2[1]])
    x.add_row([List1[2],List2[2]])
    x.add_row([List1[3],List2[3]])
    x.add_row([List1[4],List2[4]])
    x.add_row([List1[5],List2[5]])
    x.add_row([List1[6],List2[6]])
    x.add_row([List1[7],List2[7]])
    x.add_row([List1[8],List2[8]])
    x.add_row([List1[9],List2[9]])
    await client.say(":moneybag:  __***Top Ten Personnalle with Moolah***__ :moneybag: \n"+"```"+str(x)+"```"+"*Win Moolah by joining The Voice Chat and sending messages.*")

@client.command(pass_context = True)
async def buyrole(ctx,buyrole):
    '''Buy your way Up the Ladder with Moolah!' eg. .buyrole list '''
    roless = {'Royal': 250000,'The GodFather':100000,'Mod': 80000,'Intern': 50000,'Dank meme Lord':25000,'TeamMember':10000,'EliteGamerGrill':5000,'Elite':5000,'Tribune':2500}
    role = discord.utils.get(client.get_server("205438531429072897").roles, name=buyrole)
    cursor = conn.execute("SELECT NAME, COIN FROM SERVER WHERE ID=:Id", {"Id": ctx.message.author.id})
    for row in cursor:
        Name = row[0]
        coin = row[1]
    if buyrole == "list":
        x = PrettyTable()
        x.field_names = ["Roles","Moolah"]
        x.add_row(['Royal',roless['Royal']])
        x.add_row(['The GodFather',roless['The GodFather']])
        x.add_row(['Mod',roless['Mod']])
        x.add_row(['Intern',roless['Intern']])
        x.add_row(['Dank meme Lord',roless['Dank meme Lord']])
        x.add_row(['TeamMember',roless['TeamMember']])
        x.add_row(['EliteGamerGrill',roless['EliteGamerGrill']])
        x.add_row(['Elite',roless['Elite']])
        x.add_row(['Tribune',roless['Tribune']])
        await client.say(":rocket:   __***The Role Ladder***__ :rocket:  \n"+"```"+str(x)+"```"+"*Win Moolah by joining The Voice Chat and sending messages.*")
    else:
        if role != None:
            if role in ctx.message.author.roles :
                await client.say("```"+"You Already Have"+str(role)+"```")
            if roless[buyrole] != None and roless[buyrole] <= coin :
                conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (roless[buyrole], ctx.message.author.id)) 
                await client.add_roles(ctx.message.author, role)
                await client.say("```"+"You Have Bought "+str(buyrole)+"```")
            if roless[buyrole] > coin:
                await client.say("```"+"You Dont have enough Moolah for this !. You need "+str(roless[buyrole]-coin)+" more Moolah."+"\nTotal Price:"+str(roless[buyrole])+"```")
        else:
            RoleList = []
            for roles in client.get_server("205438531429072897").roles:
                RoleList.append(roles.name)
            match = get_close_matches(buyrole, RoleList)
            rolez = discord.utils.get(client.get_server("205438531429072897").roles, name=(match[0]))
            if rolez != None:
                if rolez in ctx.message.author.roles :
                    await client.say("```"+"You Already Have"+str(rolez)+"```")
                if roless[buyrole] != None and roless[buyrole] <= coin :
                    conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (roless[buyrole], ctx.message.author.id)) 
                    await client.add_roles(ctx.message.author, role)
                    await client.say("```"+"You Have Bought "+str(buyrole)+"```")
                if roless[buyrole] > coin:
                    await client.say("```"+"You Dont have enough Moolah for this !. You need "+str(roless[buyrole]-coin)+" more Moolah."+"\nTotal Price:"+str(roless[buyrole])+"```")
            else:
                await client.say("```"+'I cannot find the role you\'re trying to buy\n'
                                   'Please make sure you\'re capitalized the role name.'+"```")




def search(ctx,member):
    memberlist = ctx.message.server.members
    namelist = []
    nicklist = []
    for memberss in memberlist:
        namelist.append(memberss.name)
    match = get_close_matches(member, namelist)
    for membersx in memberlist:
        nicklist.append(str(membersx.nick))
    match2 = get_close_matches(member, nicklist)
    #print("len of match "+str(len(match)))
    #print("len of match2 "+str(len(match2)))
    if len(match) != 0 :
        #print("Got here3")
        name = discord.utils.get(memberlist, name=match[0])
        return name
    elif len(match) == 0:
        #print("Got here 3.5")
        if len(match2) != 0:
            #print("Got here4")
            nick = discord.utils.get(memberlist, nick=match2[0])
            return nick
        elif len(match2) == 0:
            #print("Got here5")
            if member.isdigit():
                nameid = discord.utils.get(memberlist, id=member)
                return nameid
            else:
                return None

betlist = []

@client.command(pass_context = True)
async def cointoss(ctx,user,amount):
    amount = abs(int(amount))
    bank = ['heads',"tails"]
    found = search(ctx,user)
    member = found
    #print(found)
    #print(member)
    Challenger = ctx.message.author
    Opponent = member
    ChallengermM = conn.execute("SELECT COIN FROM SERVER WHERE ID=:Id", {"Id": Challenger.id})
    for row in ChallengermM:
        ChallengerM = int(row[0])
    OpponentmM = conn.execute("SELECT COIN FROM SERVER WHERE ID=:Id", {"Id": Opponent.id})
    for roww in OpponentmM:
        OpponentM = int(roww[0])
    print("Challenger Moolah :"+ str(ChallengerM))
    print("Opponent Moolah :"+ str(OpponentM))
    a = ['heads', 'tails', 'cancel']
    if ChallengerM < int(amount) :
        await client.say("You Dont Have Enough Moolah for this wager!")
    elif OpponentM < int(amount) and OpponentM  > 0 :
        await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
        betlist.append(Challenger.name)
        conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (amount, Challenger.id)) 
        await client.say(str(member.name)+"has insufficient Funds for this wager! , type yes to all in!")
        confirm = await client.wait_for_message(timeout=120,author=member)
        if confirm ==None:
            await client.say("Too much time has passed!,canceling the bet!")
        if "yes" in confirm.content:
            waged = OpponentM
            await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
            await client.say("The Opponent get to pick the sides!")
            msg = await client.wait_for_message(author=member)
            if "heads" in msg.content:
                await client.say("{} has picked heads and {} takes tails ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
                conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (int(waged), member.id))

                result = secure_random.choice(bank)
                await client.say(":drum: ")
                await asyncio.sleep(3)
                await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )
                totalpot = int(amount)+int(waged)
                if result == "heads":
                    conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Opponent.id)) 
                elif result =="tails":
                    conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Challenger.id)) 
            elif "tails" in msg.content:
                totalpot = int(amount)+int(waged)
                await client.say("{} has picked tails and {} takes heads ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
                conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (int(waged), member.id))
                result = secure_random.choice(bank)
                await client.say(":drum: ")
                await asyncio.sleep(3)
                await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )

                if result == "heads":
                    conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Challenger.id)) 
                elif result =="tails":
                    conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Opponent.id)) 
            elif "cancel" in msg.content:
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (amount, Challenger.id)) 
                await client.say("{} has canceled the wager!".format(member.name))
        elif not any(x in msg.content for x in a):
        	conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (amount, Challenger.id)) 
        	await client.say("{}'s Bet Has Been canceled due to INVALID input!'".format(Challenger.name))
    elif OpponentM  == 0:
        await client.say("{} has no Moolah Left !".format(member.name))
    else:
        await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
        conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=?", (amount, Challenger.id)) 
        await client.say("The Opponent get to pick the sides!")
        waged = amount
        msg = await client.wait_for_message(timeout=120,author=member)
        if msg ==None:
            await client.say("Too much time has passed!,canceling the bet!")
        elif "heads" in msg.content:
            await client.say("{} has picked heads and {} takes tails ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
            conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (int(waged), member.id))
            result = secure_random.choice(bank)
            await client.say(":drum: ")
            await asyncio.sleep(3)
            await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )
            totalpot = int(amount)+int(waged)
            if result == "heads":
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Opponent.id)) 
            elif result =="tails":
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Challenger.id)) 
        elif "tails" in msg.content:
            totalpot = int(amount)+int(waged)
            await client.say("{} has picked tails and {} takes heads ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
            conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=? and COIN > 0", (int(waged), member.id))
            result = secure_random.choice(bank)
            await client.say(":drum: ")
            await asyncio.sleep(3)
            await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )

            if result == "heads":
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Challenger.id)) 
            elif result =="tails":
                conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (str(totalpot), Opponent.id)) 
        elif "cancel" in msg.content:
            conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (amount, Challenger.id)) 
            await client.say("{} has canceled the wager!".format(Opponent.name))
        elif not any(x in msg.content for x in a):
        	conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (amount, Challenger.id)) 
        	await client.say("{}'s Bet Has Been canceled due to INVALID input!'".format(Challenger.name))


@client.command(pass_context = True)
async def Reset(ctx):
    """RESET MOOLAH"""
    await client.say(":warning: Resetting Moolah :warning: .......")
    role = discord.utils.get(client.get_server("205438531429072897").roles, name="Primus")
    memroles = ctx.message.author.roles

    if role in memroles:
        print ("Opened database successfully")
        for members in ctx.message.server.members:
        	con = members.id
        	conn.execute("UPDATE SERVER SET COIN = ? WHERE ID=?", (0, con))
    await client.say("Moolah Corp ..Cleaning Complete! :white_sun_small_cloud: ")


DISCAPI = os.environ['DISCORDAPI']
client.run(DISCAPI)