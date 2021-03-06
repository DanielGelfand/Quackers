# creates tables for database stored in DB_FILE: alright.db
# field names created; no records
import sqlite3   #enable control of an sqlite database

DB_FILE="alright.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

def createTable(tableName, fieldNames):
	'''creates new table with list of parameters to be taken in'''
	commandArgs = "("
	colTypes = []
	for name in fieldNames:
		commandArgs += name + " " + fieldNames[name] + ","
		colTypes.append(fieldNames[name])
	commandArgs = commandArgs[:-1]
	# print(colTypes)
	commandArgs += ")"
	# print ("CREATE TABLE " + tableName + " "+ commandArgs)
	c.execute("CREATE TABLE " + tableName + " "+ commandArgs)

def closeDB():
	db.commit() #save changes
	db.close()  #close database

profilesHeader = {"UserID":"INTEGER PRIMARY KEY", "Username":"TEXT UNIQUE", "Password":"TEXT", "CalendarEvents" : "TEXT", "StarredLocations" : "TEXT"}
createTable("profiles", profilesHeader)

locationsHeader = {"LocationID" : "INTEGER PRIMARY KEY", "LocationName": "TEXT"}
createTable( "locations", locationsHeader)

eventsHeader = {"EventID":"INTEGER PRIMARY KEY", "EventName":"TEXT", "Date":"DATETIME","LocationID":"INTEGER"}
createTable("events", eventsHeader)

closeDB()
