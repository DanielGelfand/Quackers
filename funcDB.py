import sqlite3   #enable control of an sqlite database

DB_FILE="alright.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

'''BASE FUNCTIONS'''
#info is a list of fieldValues in order without primary key
def insert(tableName, info):
    '''inserts data into certain table, taking info as a list of parameters'''
    # collect Column Data Names in strings
    c.execute('PRAGMA TABLE_INFO({})'.format(tableName))
    colNames = ''
    i = 0
    for cols in c.fetchall():
        if i == 0:
            i += 1 # primary key will update itself
        else:
            colNames += "'" + cols[1] + "'"+ ','
    colNames = colNames[:-1]
    values = ''
    for val in info:
        values += "'" + str(val) + "'" + ","
    values = values[:-1]
    print("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    c.execute("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    db.commit()

def findInfo(tableName,filterValue,colToFilt,fetchOne = False, search= False):
    '''returns entire record with specific value at specific column from specified db table'''
    if search:
        filterValue = '%' + filterValue + '%'
        eq = 'LIKE'
    else:
        eq = '='
    command = "SELECT * FROM  '{0}'  WHERE {1} {3} '{2}'".format(tableName,colToFilt,filterValue, eq)
    c.execute(command)

    listInfo = []
    if fetchOne:
        info = c.fetchone()
    else:
        info = c.fetchall()

    if info:
        for col in info:
            listInfo.append(col)
    return listInfo

def modify(tableName, colToMod, newVal, filterCol, filterValue):
    print(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterIndex, filterValue))
    c.execute(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterIndex, filterValue))
    db.commit()

def delete(tableName, filterCol, filterValue):
    print(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterIndex, filterValue))
    c.execute(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterIndex, filterValue))
    db.commit()

'''SPECIFIC FUNCTIONS'''
def registerUser(username, password):
    insert('profiles', [username, password, '', ''])

def getUser(username):
    return findInfo('profiles', username, 'Username', fetchOne = True )

def addEvent(username,eventName,date,city):
    user = findInfo('profiles',username, 'Username', fetchOne = True)
    events = user[3]
    if not findInfo('events', eventName, 'EventName'):
        insert('events', [eventName, date, city])
        print('added')
    newEvent = findInfo('events',eventName, 'EventName')
    events += newEvent + ','
    modify('profiles', 'CalendarEvents', events, event,  'Username', username)

def getMyEvents(username):
    eventNames = []
    events = findInfo('profiles',username,'Username', fetchOne = True)[3]
    if events:
        for event in events.split():
            eventName = findInfo('events', event, 'EventName', fetchOne = True)
            eventNames.append(eventName)
    return eventNames
