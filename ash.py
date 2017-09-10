#join test
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import sqlite3, os
import os.path
from difflib import get_close_matches
import asyncio, random, time, json, logging
try:
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import aiohttp
import http
import praw #reddit posting
import urllib #view websites
import sys, dropbox, collections
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from prettytable import PrettyTable
from operator import ge, le, ne
global xon
sys.path.insert(0, 'modules')
from modules.sqdatabase import *
from modules.moolah import *
from modules.dropstorage import *
secure_random = random.SystemRandom()

#Initial Checks
#############################CHECKLIST TO PASS#############################
def filecheck(file,arg):
	if os.path.exists(file):
		print("[{}] Found [x]".format(file))
		return True
	elif arg == "y":
		print("{} Cannot Be found!".format(file))
		f= open("{}".format(file),"w")
		f.close()
		print("{} Created!".format(file))
	else:
		print("{} Cannot Be found!".format(file))
		return False
files = ("discord.log","data/welcome.txt")
for file in files:
	filecheck(file,"y")
###########################################################################
bot_prefix= "."
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_server_join(server):
	print("Bot has joined {}".format(server.name))
	try:
		createdatabase(server.id)
	except sqlite3.OperationalError:
		print("OperationalError! ~ Table Already Exists")
		pass
	try:
		createuserbase(server.id,server.members)
	except sqlite3.IntegrityError:
		print("IntegrityError ~ User Names Already Exists!")
		pass
	try:
		roledata = roledatabase(server)
		roledata.createroledatabase()
		roledata.populateroles()
	except sqlite3.OperationalError:
		print("OperationalError! ~ Table Already Exists")
		pass
	except sqlite3.IntegrityError:
		print("IntegrityError ~ User Names Already Exists!")
		pass

@client.event
async def on_ready():
	print("____________________________________")
	print("{} Is Now Online!".format(client.user.name))
	print("ID: {}".format(client.user.id))
	await client.change_presence(game=discord.Game(name='Doing what needs to be Done!'))
	print("____________________________________")
	restore()
	startdatabase()
	while True:
		givemoolah(client.servers)
		#############TEST AUTO BACKUP####################
		commitdatabase()
		backup()
		await asyncio.sleep(1800)

@client.event
async def on_member_join(member):
	#Send Welcome Meme!
	with open("data/welcome.txt") as f:
		line = f.readlines()
	pick = random.choice(line)
	await client.send_message(member.server.default_channel, pick)
	#Send Welcome Message!
	embed=discord.Embed(title="				   ", description="Welcome to our humble abode :island:  "+member.mention, color=0xf1ec1b)
	await client.send_message(member.server.default_channel, embed=embed)
	#Assign a role!
	role = discord.utils.get(member.server.roles, name="Recruit")
	print("Setting Role :"+str(role.name)+" Name: "+str(member.name))
	adduser(member.server.id, member)
	await client.add_roles(member, role)

@client.event
async def on_member_remove(member):
	embed=discord.Embed(title="				   ", description="Let us bid "+member.display_name+" a grand farewell from our humble abode! :wave: ", color=0xf1ec1b)
	await client.send_message(member.server.default_channel, embed=embed)

@client.event		
async def on_member_update(before, after):
	###################################STATIC NICKNAME###################################
	if "341326594113011712" in str(after.id):
		if not(before.nick == "Fiddling Bot"):
			await client.change_nickname(after, "Fiddling Bot")
			print("Reverted Music bots Nickname to Fiddling Bot")
	#if "138684247853498369" in str(after.id):
	#	if not(after.nick == "Xelor"):
	#		await client.change_nickname(after, "Xelor")
	#		print("Reverted Xelor Nickname to Xelor")
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
	##############################DATABASE UPDATE##########################################################################################
	playernameb = before.name
	playernamea = after.name
	playernickb = before.nick

	playernicka = after.nick
	if playernameb != playernamea:
		red = database(serverid=after.server.id,id=after.id)
		red.update(arg="name",DATA=after.name)
	if playernickb != playernicka:
		red = database(serverid=after.server.id,id=after.id)
		red.update(arg="nick",DATA=after.nick)

@client.event
async def on_message(message):
	await client.process_commands(message)
	authorr = message.author
	contents = message.content
	print("Name: [{}]".format(authorr.name)+" Nickname: [{}]".format(authorr.nick)+" ID: [{}]".format(authorr.id)+" String Length:"+str(len(message.content)))
	#############################################################GIVE COINS#############################################################
	number = 1
	if not "." in message.content[0:1] and not "!" in message.content[0:1] :
		if authorr != None and authorr.bot != True:
			red = database(serverid=message.server.id,id=authorr.id)
			red.update(arg="coin",DATA=number,types="+")
	####################################################################################################################################
	if authorr.name != "Innocent Bot":
		if len(message.content) > 850 :
			await client.delete_message(message)
			warningmsg1 = await client.send_message(message.channel, "Sorry Buddy you have crossed the Character Limit(1000) around these parts! :sunglasses:")
			warningmsg2 = await client.send_message(message.channel, "If u have any Complaints take it to Hawkens™,or the Suggestion Box \n You know what , take all the Complaints to Hawkens™ :joy: ")
			await asyncio.sleep(2)
			await client.delete_message(warningmsg1)
			await client.delete_message(warningmsg2)

	#######################################################################################################################################

#################################COMMANDS#########################################
@client.command(pass_context = True)
async def getbans(ctx):
	"""Get the List of Currently Banned People"""
	x = await client.get_bans(ctx.message.server)
	x = '\n'.join([y.name for y in x])
	embed = discord.Embed(title = "List of Banned Members", description = x, color = 0xFFFFF)
	return await client.say(embed = embed)

@client.command(pass_context = True)
async def shutdown(ctx):
	"""SAVES ALL USER DATA and turns off the bot/restart"""
	if ctx.message.author.server_permissions.administrator:
		print("Saving Files to Dropbox")
		closedatabase()
		backup()
		warning = await client.say("Saving Data Files....")
		await asyncio.sleep(1.2)
		warning2 = await client.say("Shutting Down....")
		await asyncio.sleep(1.2)
		await client.delete_message(warning)
		await client.delete_message(warning2)
		await asyncio.sleep(1.2)
		await client.logout()
		try:
			sys.exit()
		except:
			pass
	else:
		warning3 = await client.say("You Dont Have the Permissions Mate")
		await asyncio.sleep(1.2)
		await client.delete_message(warning3) 

@client.command(pass_context=True)
async def echo(ctx, *, echo: str):
	"""The Bot follows your lead!"""
	if ctx.message.author.server_permissions.administrator:
		await client.delete_message(ctx.message)
		await client.say(echo)
	else:
		await client.say("Sorry Bro , you dont have permissions for this !")
	
@client.command(pass_context=True)
async def kill(ctx, *, member):
	"""Kills the Given Target (kick)"""
	member =search(ctx,member)
	if ctx.message.author.server_permissions.administrator:
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

def search(ctx,member):
	member = member.lower()
	memberlist = ctx.message.server.members
	namelist = []
	nicklist = []
	for memberss in memberlist:
		namelist.append(memberss.name)
	match = get_close_matches(member, namelist)
	for xx in match:
		print(str(xx))
	for membersx in memberlist:
		nicklist.append(str(membersx.nick))
	match2 = get_close_matches(member, nicklist)
	if len(match) != 0 :
		print("Got here3")
		name = discord.utils.get(memberlist, name=match[0])
		return name
	elif len(match) == 0:
		print("Got here 3.5")
		if len(match2) != 0:
			print("Got here4")
			nick = discord.utils.get(memberlist, nick=match2[0])
			return nick
		elif len(match2) == 0:
			print("Got here5")
			if member.isdigit():
				nameid = discord.utils.get(memberlist, id=member)
				return nameid
			elif "@" in member[1:2]:
				print(member[1:2])
				user = member.strip('<')
				user = user.strip('>')
				user = user.strip('@')
				user = user.strip('!')
				print("PRINTING "+user)
				user = discord.utils.get(ctx.message.server.members, id=user)
				print(user.display_name)
				return user
			else:
				return None

def check(message):
	global memberpurge
	if message.author == memberpurge:
		return True
	else:
		return False

@client.command(pass_context=True)
async def clear(ctx,messages=0,member=None):
	'''Clears a number of messages or a specified person's messages!'''
	if messages == 0 and member ==None:
		await client.say("No Input ! (.clear <e.g 10> <member or leave as blank> ")
	if member == None and messages !=0:
		mgs = [] #Empty list to put all the messages in the log FOR 14 DAYS OR BELOW
		number = int(messages) #Converting the amount of messages to delete to an integer
		async for x in client.logs_from(ctx.message.channel, limit = number):
			mgs.append(x)
		await client.delete_messages(mgs)
	elif member != None and messages!=0:
		global memberpurge
		memberpurge = search(ctx,member)
		await client.purge_from(channel=ctx.message.channel,check=check,limit=messages,)

	
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


@client.command(aliases=['lovecalc'],pass_context=True)
async def lovecalculator(ctx,lovers,loved):
	'''Find out your true love with the 100% totally accurate love calculator!'''
	lovers = search(ctx,lovers)
	loved = search(ctx,loved)
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


global checklist2
checklist2 = []
@client.command(aliases=['compli'],pass_context=True)
async def compliment(ctx,member):
	'''Brighten Up Someone's day by complimenting them!'''
	global checklist2
	user = search(ctx,member)
	with open('data\Scraped-Insults-Compliments\compliments.txt', encoding='utf-8', mode="r") as f:
		data = f.readlines()
	if user.bot:
		with open('data\Scraped-Insults-Compliments\compliments-Robot.txt', encoding='utf-8', mode="r") as f:
			data = f.readlines()
	data = [x.strip('\n') for x in data]
	data = filter(lambda x: x not in checklist2, data)
	data = list(data)
	x1 = user.id
	msg = ' '
	if user != None:
		if user.display_name == "Innocent Bot":
			user = ctx.message.author
			msg = "Awww How Sweet!,You Brighten my Day.Alas...if only I could feel.."
			await client.say(user.mention + msg)
		else:
			#await client.delete_message(ctx.message)
			xx = random.choice(data)
			await client.say(user.mention + msg + xx)
			checklist2.append(xx)
	else:
		#await client.delete_message(ctx.message)
		xx =random.choice(data)
		await client.say(ctx.message.author.mention + msg + xx)
		checklist2.append(xx)
	if len(data) == len(checklist2):
		checklist2 = []

checklist1 = []

@client.command(pass_context=True)
async def insult(ctx,user):
	'''Wasn't stating the obvious enough for your dull mind?'''
	user = search(ctx,user)
	global checklist1

	"""Insults The specified User (HARSH ROASTS)"""
	def _read_json():
		with open('data\Scraped-Insults-Compliments\insults.json', encoding='utf-8', mode="r") as f:
			data = json.load(f)
		return data
	insults =_read_json()
	insults = filter(lambda x: x not in checklist1, insults)
	insults = list(insults)
	x1 = user.id
	msg = ' '
	if user != None:
		if user.display_name == "Innocent Bot":
			user = ctx.message.author
			msg = " How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
			await client.say(user.mention + msg)
		else:
			#await client.delete_message(ctx.message)
			xx = random.choice(insults)
			await client.say(user.mention + msg + xx)
			checklist1.append(xx)
	else:
		#await client.delete_message(ctx.message)
		xx = random.choice(insults)
		await client.say(ctx.message.author.mention + msg + xx)
		checklist1.append(xx)
	if len(insults) == len(checklist1):
		checklist1 = []

@client.command(pass_context = True)
async def userinfo(ctx,member=None):
	"""Gets User Info"""
	if member == None:
		memberz = ctx.message.author
		red = database(serverid=ctx.message.server.id,id=memberz.id)
		info = red.info()
		print(info.name)
		embed=discord.Embed(title="User Information :", color=(memberz.top_role.color))
		embed.set_thumbnail(url=memberz.avatar_url)
		embed.add_field(name="Name", value=info.name, inline=True)
		embed.add_field(name="Nick", value=info.nick, inline=True)
		embed.add_field(name="ID", value=info.id, inline=True)
		embed.add_field(name="Moolah", value='**'+str(info.coin)+"**", inline=True)
		await client.say(embed=embed)
	else:
		memberz = search(ctx,member)
		if memberz != None:
			print(memberz.id)
			red = database(serverid=ctx.message.server.id,id=memberz.id)
			info = red.info()
			embed=discord.Embed(title="User Information :", color=(memberz.top_role.color))
			embed.set_thumbnail(url=memberz.avatar_url)
			embed.add_field(name="Name", value=info.name, inline=True)
			embed.add_field(name="Nick", value=info.nick, inline=True)
			embed.add_field(name="ID", value=info.id, inline=True)
			embed.add_field(name="Moolah", value='**'+str(info.coin)+"**", inline=True)
			#fix = "Joined at: "+str(memberz.joined_at)
			#fix = fix[0:30]
			#embed.set_footer(text=fix)
			await client.say(embed=embed)
		else:
			await client.say("**{}** not found! , Contact your bruh .".format(member))

@client.command(pass_context = True)
async def addcoin(ctx,member,number):
	"""Gives Moolah to specified user Ultra Admin use only"""
	if ctx.message.author.server_permissions.administrator:
		print ("Opened database successfully")
		memberz = search(ctx,member)
		if memberz != None:
			red = database(serverid=ctx.message.server.id,id=memberz.id)
			red.update(arg="coin",DATA=number,types="+")
			await client.say("No.of Moolah Added: "+str(number))

@client.command(pass_context = True)
async def removecoin(ctx,member,number):
	"""Removes Moolah from specified user Ultra Admin use only"""
	if ctx.message.author.server_permissions.administrator:
		print ("Opened database successfully")
		memberz = search(ctx,member)
		if memberz != None:
			red = database(serverid=ctx.message.server.id,id=memberz.id)
			red.update(arg="coin",DATA=number,types="-")
			await client.say("No.of Moolah Added: "+str(number))

@client.command(pass_context = True)
async def topdog(ctx):
	'''Shows the Top 10 Holders of Moolah '''
	red = database(serverid=ctx.message.server.id)
	string = red.top10()
	x = PrettyTable()
	x.field_names = ["Names","Moolah"]
	for y in range(0,9):
		x.add_row([string.Listncoin[y],string.Listcoin[y]])
	await client.say(":moneybag:  __***Top Ten Personnalle with Moolah***__ :moneybag: \n"+"```"+str(x)+"```"+"*Win Moolah by joining The Voice Chat and sending messages.*")

global costs
global d
d = collections.defaultdict(list)
@client.command(pass_context = True)
async def buytic(ctx,NoTic=None):
	'''buy a raffle ticket!'''
	global xon
	if NoTic == None:
		await client.say("```Please input the No of tickets to be purchased!. e.g- .buytic 5 \n Each Ticket costs {}```".format(costs))
	else:
		NoTic = abs(int(NoTic))
		c1 =database(serverid=ctx.message.server.id,id = ctx.message.author.id) 
		info = c1.info()
		if info.coin < int(costs)*int(NoTic):
			await client.say("You Dont Have Enough Moolah for this Purchase")
		if NoTic > Max:
			await client.say("Maximum Numer of Tickets per person for this raffle is {}".format(Max))
		elif NoTic <=int(xon) and not info.coin < int(costs)*int(NoTic):
			totalcost = 0 
			nott = 0
			rafflelist.append(ctx.message.author.name)
			global d
			print(d[ctx.message.author.name])
			for x in range (0,NoTic):
				if len(raffletic) != 0 and len(d[ctx.message.author.name]) != Max:
					number = random.choice(raffletic)
					nott = nott + 1
					totalcost = totalcost + int(costs)
					d[ctx.message.author.name].append(number)
					raffletic.remove(number)
			print(d[ctx.message.author.name])
			global pool
			pool = pool + totalcost
			xon = int(xon) - abs(int(nott))
			await client.say("```{} Tickets Bought Costing {}\n [{}] remaining tickets. Current Pool [{}] Moolah ```\n Your Numbers are **".format(nott,totalcost,xon,pool)+str(d[ctx.message.author.name])+"**.")
			c1.update(arg="coin",types ="-",DATA=totalcost)
			print(d)

@client.command(pass_context = True)
async def callraffle(ctx):
	'''End a raffle and draw the numbers !'''
	global RaffleSTATE
	if ctx.message.author.server_permissions.administrator and RaffleSTATE ==True:
		await client.say("The time to Buy Tickets has ended ! \n Drawing a number from the magical Hat!")
		await client.say(":drum: ")
		await asyncio.sleep(3)
		global winningno
		winningno = random.choice(list(range(0, int(xon))))
		for x in d:
			for y in d[x]:
				while winningno != y:
					print(winningno)
					winningno = random.choice(list(range(0, int(xon))))
					global final
					final = x
		await client.say("The Winning Number is {} !".format(winningno))
		await client.say("Whoever is holding the winning number please come foward and claim your prize!")
		await asyncio.sleep(10)
		await client.say("{} is holding the the winning number {}".format(x,winningno))
		print(final)
		c1 =database(serverid=ctx.message.server.id,id = (search(ctx,final)).id)
		global pool
		c1.update(arg="coin",types ="+",DATA=pool)
		RaffleSTATE = False

global RaffleSTATE
RaffleSTATE = False
rafflelist = []
global xon
xon = 0
global raffletic
global pool
pool = 0

raffletic = list(range(0, xon))
@client.command(pass_context = True)
async def startraffle(ctx,nooftickets=None,MaxticketsPERPERSON=0,cost=None):
	'''Start a raffle '''
	if nooftickets ==None:
		await client.say("```Please input the No of tickets to be purchased!```")
	elif cost ==None:
		await client.say("```Please input the price of each ticket!```")
	elif MaxticketsPERPERSON ==0:
		await client.say("```Please input The Maximum number of tickets per person!```") 
	if ctx.message.author.server_permissions.administrator:
		global RaffleSTATE
		if RaffleSTATE == False:
			if nooftickets !=None and cost !=None and MaxticketsPERPERSON != 0:
				global costs
				costs = cost
				global xon
				global Max
				Max = MaxticketsPERPERSON
				xon = nooftickets
				global raffletic
				raffletic = list(range(0, int(xon)))
				await client.say("``` A Raffle has been Started by [{}] \n Maximum of {} tickets per person. Each Tickets Costs {} Moolah \n No of Tickets Left {}```".format(ctx.message.author.display_name,Max,cost,xon))
				RaffleSTATE = True
		else:
			await client.say("There is Already a Raffle Going On!")

@client.command(pass_context = True)
async def Reset(ctx):
	"""RESET MOOLAH"""
	if ctx.message.author.server_permissions.administrator:
		await client.say(":warning: Resetting Moolah :warning: ....... Type [yes/no] to Confirm!.")
		print ("Opened database successfully")
		red = database(serverid="205438531429072897")
		string = red.update(0,"masscoin",types="=")
		await client.say("Moolah Corp ..Cleaning Complete! :white_sun_small_cloud: ")
	else:
		await client.say("You dont have the Permissions for this ! , Contact your local Admin for more info.")

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

async def get_response(author, text):
	payload = {}
	payload["key"] = 'CC2qmlHtqo3Auq4DSQk-d8oAzjQ'
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

betlist = []

@client.command(pass_context = True)
async def cointoss(ctx,user,amount):
	''' Wager Your Moolah in this deadly game and rise to the top!'''
	print(betlist)
	amount = abs(int(amount))
	bank = ['heads',"tails"]
	a = ['heads', 'tails', 'cancel']
	member = search(ctx,user)
	Opponent = member
	Challenger = ctx.message.author
	blue = database(serverid=ctx.message.server.id,id=ctx.message.author.id)
	red = database(serverid=ctx.message.server.id,id=Opponent.id)
	redm = red.info().coin
	bluem = blue.info().coin
	print("Challenger Moolah: "+str(bluem))
	print("Opponent Moolah: "+str(redm))
	if bluem < amount :
		await client.say("You Dont Have Enough Moolah for this wager!")
	if Challenger.name in betlist:
		await client.say("There is already a Pending bet!")
	elif Challenger.name not in betlist:
		if redm < amount and redm  > 0 and not bluem < amount:
			if Challenger.name not in betlist:
				print("APPENDING!")
				betlist.append(Challenger.name)
				betlist.append(Opponent.name)
			await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
			await client.say("** ``` Warning! {} has less then the Wagered amount! [{}] ```**.\n Your Opponent Can All in and Gain the Total Pot of **{}** .\n Type **[yes/no]** to **[Confirm/Cancel]** .".format(member.name,redm,(redm+amount)))
			confirmation = await client.wait_for_message(timeout=120,author=ctx.message.author)
			if "yes" in confirmation.content:
				blue.update(amount,"coin","-")
				await client.say("```"+str(member.name)+" has insufficient Funds for this wager! .```\n Type **yes** to all in! ")
				confirm = await client.wait_for_message(timeout=120,author=member)
				if confirm ==None:
					await client.say("Too much time has passed!,canceling the bet!")
					blue.update(amount,"coin","+")
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
				if "yes" in confirm.content:
					waged = redm
					await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
					await client.say("The Opponent get to pick the sides!")
					msg = await client.wait_for_message(timeout=120,author=member)
					if "heads" in msg.content:
						betlist.remove(Challenger.name)
						betlist.remove(Opponent.name)
						await client.say("{} has picked heads and {} takes tails ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
						red.update(waged,"coin","-")
						result = secure_random.choice(bank)
						await client.say(":drum:")
						await asyncio.sleep(3)
						await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )
						totalpot = amount+int(waged)
						if result == "heads":
							red.update(totalpot,"coin","+")
						elif result =="tails":
							blue.update(totalpot,"coin","+")
					elif "tails" in msg.content:
						betlist.remove(Challenger.name)
						betlist.remove(Opponent.name)
						totalpot = amount+int(waged)
						await client.say("{} has picked tails and {} takes heads ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
						red.update(waged,"coin","-")
						result = secure_random.choice(bank)
						await client.say(":drum:")
						await asyncio.sleep(3)
						await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )

						if result == "heads":
							blue.update(totalpot,"coin","+") 
						elif result =="tails":
							red.update(totalpot,"coin","+") 
					elif "cancel" in msg.content:
						betlist.remove(Challenger.name)
						betlist.remove(Opponent.name)
						blue.update(amount,"coin","+") 
						await client.say("{} has canceled the wager!".format(member.name))
					elif not any(x in msg.content for x in a):
						betlist.remove(Challenger.name)
						betlist.remove(Opponent.name)
						blue.update(amount,"coin","+")  
						await client.say("{}'s Bet Has Been canceled due to INVALID input!'".format(Challenger.name))
				elif not any(x in msg.content for x in a):
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
					blue.update(amount,"coin","+") 
					await client.say("{}'s Bet Has Been canceled due to INVALID input!'".format(Challenger.name))
			else:
				betlist.remove(Challenger.name)
				betlist.remove(Opponent.name)
				await client.say("The Wager has been canceled by "+str(Challenger.name))
		elif redm  == 0:
			await client.say("{} has no Moolah Left !".format(member.name))
		else:
			if Challenger.name not in betlist and bluem > amount and bluem > 0:
				betlist.append(Challenger.name)
				betlist.append(Opponent.name)
				await client.say("Showdown between {} and {} for ".format(ctx.message.author.mention,member.mention) +"\n"+"Challenger Has Waged " +"**"+str(amount)+"**" +" Moolah")
				blue.update(amount,"coin","-") 
				await client.say("The Opponent get to pick the sides!")
				waged = amount
				msg = await client.wait_for_message(timeout=120,author=member)
				if msg ==None:
					await client.say("Too much time has passed!,canceling the bet!")
					blue.update(amount,"coin","+") 
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
				elif "heads" in msg.content:
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
					await client.say("{} has picked heads and {} takes tails ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
					red.update(int(waged),"coin","-") 
					result = secure_random.choice(bank)
					await client.say(":drum: ")
					await asyncio.sleep(3)
					await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )
					totalpot = amount+int(waged)
					if result == "heads":
						red.update(int(totalpot),"coin","+") 
					elif result =="tails":
						blue.update(int(totalpot),"coin","+") 
				elif "tails" in msg.content:
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
					totalpot = amount+int(waged)
					await client.say("{} has picked tails and {} takes heads ".format(member.name,ctx.message.author.name)+"{} has waged {}. \n **Total Pot:{}**".format(member.name,waged,str(int(waged)+int(amount))))
					red.update(int(waged),"coin","-") 
					result = secure_random.choice(bank)
					await client.say(":drum: ")
					await asyncio.sleep(3)
					await client.say("The Coin has Landed !.........and its "+"**"+str(result)+" ! **" )

					if result == "heads":
						blue.update(int(totalpot),"coin","+")  
					elif result =="tails":
						red.update(int(totalpot),"coin","+")
				elif "cancel" in msg.content:
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
					blue.update(amount,"coin","+")  
					await client.say("{} has canceled the wager!".format(Opponent.name))
				elif not any(x in msg.content for x in a):
					betlist.remove(Challenger.name)
					betlist.remove(Opponent.name)
					blue.update(amount,"coin","+")  
					await client.say("{}'s Bet Has Been canceled due to INVALID input!'".format(Challenger.name))
			elif Challenger.name in betlist:
				await client.say("There is already a Pending Bet!")
			else:
				await client.say("Error Bet Couldn't be Placed!")

@client.command(pass_context = True)
async def highlow(ctx,rounds=8):
	'''Lets you play High and Low - Entry Costs Only 1 Moolah '''
	baseamount = 1
	red = database(serverid=ctx.message.server.id,id=ctx.message.author.id)
	if red.info().coin > baseamount:
		red.update(baseamount,"coin","-")
		cards = range(1, 14)
		faces = {11: 'Jack', 12: 'Queen', 13: 'King', 1: 'Ace'}
		suits = ["Spades", "Hearts", "Clubs", "Diamonds"]

		comparisons = {'h': le, 'l': ge, 's': ne}
		pass_template = "```Good job! The card is the {0} of {1}.```"
		fail_template = "```Sorry, you fail. The card is the {0} of {1}.```"
		running = True
		card = random.choice(cards)
		suit = random.choice(suits)
		while running:
			await client.say("```The first card is the {0} of {1}.```".format(faces.get(card,card),suit))
			next_card = random.choice(cards)
			next_suit = random.choice(suits)
			await client.say("Higher (H), Lower (L) or the Same (S)? "+"Current Pot: [**"+str(baseamount)+"**]")
			ui = await client.wait_for_message(timeout=120,author=ctx.message.author)
			choices = set("hls")
			if ui.content.lower() in choices:
				ui = ui.content.lower()
			if comparisons[ui](next_card, card):
				await client.say(fail_template.format(faces.get(next_card,next_card),next_suit))
				break		   
			else:
				await client.say(pass_template.format(faces.get(next_card,next_card),next_suit))
				if baseamount < 1000:
					baseamount = baseamount+(baseamount)
					multiplyer = 2
				elif baseamount >= 1000 and baseamount < 2999:
					baseamount = baseamount+(baseamount/2)
					multiplyer = 1.5
				elif baseamount > 2999:
					baseamount = baseamount+(baseamount/4)
					multiplyer = 1.25
				await client.say("```Do you want to continue playing ? type [Y/n]. \n Current Multiplier [x{}] Current Pot [{}]```".format(str(multiplyer),str(baseamount)))
				repeat = await client.wait_for_message(timeout=120,author=ctx.message.author)
				repeat = repeat.content.lower()
				if repeat != "yes" and repeat != "y":
					running = False
					red.update(baseamount,"coin","+")
					await client.say("Have Fun with your Moolah! Alas for me 'tis a goodbye amigo.")
				card = next_card
				suit = next_suit
	else:
		await client.say("You dont have enough Moolah")

@client.command(pass_context = True)
async def sellrole(ctx,sellrole,price):
	'''Sets a Role for sale'''
	rolelist = []
	if ctx.message.author.server_permissions.administrator:
		for rolea in ctx.message.server.roles:
			rolelist.append(rolea.name)
		match = get_close_matches(sellrole, rolelist)
		found = discord.utils.get(ctx.message.server.roles, name=match[0])
		sale = 1
		roledatabase(ctx.message.server).setrolesale(found,sale,price)

@client.command(pass_context = True)
async def buyrole(ctx,buyrole=None):
	if buyrole == None:
		string = roledatabase(ctx.message.server)
		userinfo = string.showrolesale()
		userlist = userinfo.namelist
		print(userlist)
		usercoinlist = userinfo.coinlist
		print(usercoinlist)
		x = PrettyTable()
		for y in range(0,len(usercoinlist)):
			x.field_names = ["Roles","Moolah"]
			x.add_row([userlist[y],usercoinlist[y]])
		await client.say(":moneybag:  __***Roles to purchase with Moolah***__ :moneybag: \n"+"```"+str(x)+"```"+"*Win Moolah by joining The Voice Chat and sending messages.*")
	else:
		rolelist = []
		for rolea in ctx.message.server.roles:
			rolelist.append(rolea.name)
		match = get_close_matches(buyrole, rolelist)
		if len(match) !=0:
			found = discord.utils.get(ctx.message.server.roles, name=match[0])
			print("GOT HERES")
			roledata = roledatabase(server=ctx.message.server).info(input=found.id)
			attrs = vars(roledata)
			print(attrs)
			print("GOT HERES")
		else:
			match =None
		red = database(serverid=ctx.message.server.id,id=ctx.message.author.id)
		userinfo = red.info()
		if match != None:
			if roledata.sale == 0:
				await client.say("Role NOT for SALE!")
			elif roledata.sale == 1 and userinfo.coin >= roledata.coin:
				await client.say("Role for SALE!")
			elif userinfo.coin < roledata.coin:
				await client.say("You do not have enough Moolah for the purchase!.")
			else:
				await client.say("Error Occurred when trying to purchase [{}] .".format(found.name))
		else:
			await client.say("{} Not Found on the Server!.".format(buyrole))

@client.command(pass_context = True)
async def test(ctx):
	if ctx.message.author.server_permissions.administrator:
		try:
			await client.say("RUNNING")
			roledata = roledatabase(ctx.message.server)
			roledata.createroledatabase()
			roledata.populateroles()
			await client.say("Finished")
		except:
			print("Error")

DISCAPI = os.environ['DISCORDAPI']
client.run(DISCAPI)