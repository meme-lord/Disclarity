import sqlite3

conn = sqlite3.connect('USER.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE SERVER
         (ID INT PRIMARY KEY     NOT NULL,NAME           TEXT    NOT NULL,NICK            TEXT    NOT NULL,ROLE        TEXT    NOT NULL,COIN         INT     NOT NULL);''')
print ("Table created successfully")


cursor = conn.execute("SELECT ID, NAME, NICK, COIN from SERVER")
for row in cursor:
   print( "ID = ", row[0])
   print ("NAME = ", row[1])
   print ("NICK = ", row[2])
   print( "COIN = ", row[3], "\n")



conn.close()