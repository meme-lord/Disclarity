import sqlite3
global conn


class database:
	def __init__(self,name = None ,nick=None,id =None,coin = 0):
		self.id = id
		cursor = conn.execute("SELECT NAME, NICK, ID,COIN FROM SERVER WHERE ID=:Id", {"Id": self.id})
		for row in cursor:
			self.name = row[0]
			self.nick=  row[1]
			self.id =   row[2]
			self.coin = row[3]
	def info(self):
		return self
	def update(self,arg,DATA,types = None):
		if arg == "name":
			conn.execute("UPDATE SERVER SET NAME = ? WHERE ID=?", (DATA, self.id)) 
			print("Changed Name From "+str(self.name) +" to "+str(DATA))
			self.name = DATA
			return self
		if arg == "nick":
			conn.execute("UPDATE SERVER SET NICK = ? WHERE ID=?", (DATA, self.id)) 
			print("Changed Nick From "+str(self.nick) +" to "+str(DATA))		
			self.nick = DATA
			return self
		if arg == "coin":
			if types == "+":
				conn.execute("UPDATE SERVER SET COIN = COIN + ? WHERE ID=?", (DATA, self.id)) 
				print("Added "+str(DATA)+" Moolah to "+ str(self.name))	
				ncoin = conn.execute("SELECT COIN FROM SERVER WHERE ID=:Id", {"Id": self.id})
				for row in ncoin:
					self.coin = row[0]
				return self
			elif types == "-":
				conn.execute("UPDATE SERVER SET COIN = COIN - ? WHERE ID=?", (DATA, self.id)) 
				print("Subtracted "+str(DATA)+" Moolah From "+ str(self.name))	
				ncoin = conn.execute("SELECT COIN FROM SERVER WHERE ID=:Id", {"Id": self.id})
				for row in ncoin:
					self.coin = row[0]
				return self