import sqlite3
global conn
import logging
logger = logging.getLogger(__name__)

class roledatabase:
	def __init__(self,server):
		self.server = server
		self.serverid = server.id
		self.servername = server.name
	def createroledatabase(self):
		logging.info("Creating a ROLE table for {}".format(self.servername))#
		conn.execute("CREATE TABLE  SERVERROLES_"+self.serverid+"(ID INT PRIMARY KEY     NOT NULL,NAME           TEXT    NOT NULL,SALE          INT     NOT NULL,COIN         INT     NOT NULL)")	
		conn.commit()
	def info(self,input):
		cursor = conn.execute("SELECT ID, NAME, SALE,COIN FROM SERVERROLES_"+self.serverid+" WHERE ID=:id",{"id": input})
		for row in cursor:
			self.id   =	row[0]
			self.name =	row[1]
			self.sale =	row[2]
			self.coin =	row[3]
		return self

	def populateroles(self):
		for roles in self.server.roles:
			conn.execute("INSERT INTO SERVERROLES_"+self.serverid+" VALUES (?, ?, ?, ?);", (roles.id, roles.name, 0,0))
			conn.commit()	
	def setrolesale(self,role=None,sale=0,roleprice=0):
		conn.execute("UPDATE SERVERROLES_"+self.serverid+" SET SALE = ? WHERE ID=?", (sale, role.id))
		conn.execute("UPDATE SERVERROLES_"+self.serverid+" SET COIN = ? WHERE ID=?", (roleprice, role.id))
		conn.commit() 
	def showrolesale(self):
		cursor = conn.execute("SELECT `_rowid_`,* FROM SERVERROLES_"+self.serverid+" WHERE `SALE` LIKE '%1%' ")
		self.namelist = []
		self.coinlist = []
		for row in cursor:
			self.namelist.append(row[2])
			self.coinlist.append(row[4])
			logging.info("Printing Name:"+str(row[1])+" Printing Row 2 (coin): "+str(row[3]))
		return self

	def update(self,ROLE,arg):
		if arg == name:
			logging.info("{} Server Role Name Changed from {} to {}".format(self.servername,))
			conn.execute("UPDATE SERVER_"+self.serverid+" SET NAME = ? WHERE ID=?", (ROLE.name, self.id)) 

def createdatabase(serverid):
	logging.info("Creating A new server table!")
	conn.execute("CREATE TABLE  SERVER_"+serverid+"(ID INT PRIMARY KEY     NOT NULL,NAME           TEXT    NOT NULL,NICK            TEXT    ,ROLE        TEXT    NOT NULL,COIN         INT     NOT NULL)")	
	conn.commit()

def createuserbase(serverid,members):
	for x in members:
		ID2 = int(x.id)
		NAME2 = str(x.name)
		NICK2 = str(x.nick)
		ROLE2 = str(x.top_role)
		COIN = int(0)
		conn.execute("INSERT INTO SERVER_"+serverid+" VALUES (?, ?, ?, ?, ?);", (ID2, NAME2, NICK2, ROLE2, COIN))
		conn.commit()

def adduser(serverid,member):
	ID2 = int(member.id)
	NAME2 = str(member.name)
	NICK2 = str(member.nick)
	ROLE2 = str(member.top_role)
	COIN = int(0)
	conn.execute("INSERT INTO SERVER_"+serverid+" VALUES (?, ?, ?, ?, ?);", (ID2, NAME2, NICK2, ROLE2, COIN))
	conn.commit()

def startdatabase():
	global conn
	logging.info("Starting database")
	conn = sqlite3.connect('USER.db') 
def commitdatabase():
	global conn
	conn.commit()

def closedatabase():
	logging.info("Closing Database!")
	global conn
	try:
		conn.commit()
		conn.close()
	except:
		logging.warning("Error Closing Database!")

class database:
	def __init__(self,serverid=None,name = None ,nick=None,id =None,coin = 0):
		self.serverid = serverid
		if id ==None:
			cur = conn.cursor()
			cur.execute("SELECT NAME, NICK, ID,COIN FROM SERVER_"+serverid)
			rows = cur.fetchall()
			self.name = []
			self.nick=  []
			self.id =   []
			self.coin = []
			for row in rows:
				self.name.append(row[0])
				self.nick.append(row[1])
				self.id.append(row[2])
				self.coin.append(row[3])
		else:
			self.id = id
			cursor = conn.execute("SELECT NAME, NICK, ID,COIN FROM SERVER_"+serverid+" WHERE ID=:id",{"id": id})
			for row in cursor:
				self.name = row[0]
				self.nick=  row[1]
				self.id =   row[2]
				self.coin = row[3]
	def info(self):
		return self
	def update(self,DATA,arg,types=None):
		if arg == "name":
			conn.execute("UPDATE SERVER_"+self.serverid+" SET NAME = ? WHERE ID=?", (DATA, self.id)) 
			logging.info("Changed Name From "+str(self.name) +" to "+str(DATA))
			self.name = DATA
			return self
		if arg == "nick":
			conn.execute("UPDATE SERVER_"+self.serverid+" SET NICK = ? WHERE ID=?", (DATA, self.id)) 
			logging.info("Changed Nick From "+str(self.nick) +" to "+str(DATA))		
			self.nick = DATA
			return self
		if arg == "coin":
			if types == "+":
				conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = COIN + ? WHERE ID=?", (DATA, self.id)) 
				logging.info("Added "+str(DATA)+" Moolah to "+ str(self.name))	
				ncoin = conn.execute("SELECT COIN FROM SERVER_"+self.serverid+" WHERE ID=:Id", {"Id": self.id})
				for row in ncoin:
					self.coin = row[0]
				return self
			elif types == "-":
				conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = COIN - ? WHERE ID=?", (DATA, self.id)) 
				logging.info("Subtracted "+str(DATA)+" Moolah From "+ str(self.name))	
				ncoin = conn.execute("SELECT COIN FROM SERVER_"+self.serverid+" WHERE ID=:Id", {"Id": self.id})
				for row in ncoin:
					self.coin = row[0]
				return self
			elif types == "=":
				for row in self.id:
					conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = ? WHERE ID=?", (DATA, row))
		if arg == "masscoin":
			if types == "+":
				for row in self.id:
					conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = COIN + ? WHERE ID=?", (DATA, row))
			if types == "-":
				for row in self.id:
					conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = COIN - ? WHERE ID=?", (DATA, row))
			if types == "=":
				for row in self.id:
					conn.execute("UPDATE SERVER_"+self.serverid+" SET COIN = ? WHERE ID=?", (DATA, row))

	def top10(self):
		cursor = conn.execute(" SELECT NAME, COIN FROM SERVER_"+self.serverid+" ORDER BY COIN DESC LIMIT 10")
		self.Listncoin = []
		self.Listcoin = []
		for row in cursor:
			Name = row[0]
			coin = row[1]
			self.Listncoin.append(Name)
			self.Listcoin.append(coin)
		return self
	def getvolume(self):
		self.volume = 0
		for coin in self.coin:
			self.volume = self.volume+coin
		return self