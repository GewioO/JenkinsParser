import psycopg2

cur = 0
con = 0

def databaseConnection():
      global con
      con = psycopg2.connect(
      database = "UserLink",
      user     = "postgres",
      password = "",
      host     = "localhost",
      port     = "5432"
)

def db_setLink(name, link):
      databaseActions(0)
      if isExist(name) == True:
            cur.execute("UPDATE USERINFO set link = "+postgresString(link)+" where U = "+postgresString(name)+"")
      else:
            insertNewUser(name, link, "", "", "300")
            
      databaseActions(1)
            
def db_getLink(name):
      databaseActions(0)
      _,_, linkInTable, _,_,_ = getRowValues(name)
      databaseActions(1)
      return linkInTable

def db_setPath(name, path):
      databaseActions(0)
      if isExist(name) == True:
            cur.execute("UPDATE USERINFO set BUILD_PATH = "+postgresString(path)+" where U = "+postgresString(name)+"")
      else:
            insertNewUser(name, "", path, "", "300")

      databaseActions(1)
      return str(path)

def db_getPath(name):
      databaseActions(0)
      _,_,_, path, _,_ = getRowValues(name) 
      databaseActions(1)
      return path

def db_setNumber(name, number):
      databaseActions(0)
      if isExist(name) == True:
            cur.execute("UPDATE USERINFO set BUILD_NUMBER = "+postgresString(number)+" where U = "+postgresString(name)+"")
      else:
            insertNewUser(str(name), "", "", str(number), "300")

      databaseActions(1)
      return str(number)

def db_getNumber(name):
      databaseActions(0)
      _,_,_,_, number, _ = getRowValues(name)
      databaseActions(1)
      return number

def db_setTime(name, time):
      databaseActions(0)
      if isExist(name) == True:
            cur.execute("UPDATE USERINFO set MESSAGE_TIME = "+postgresString(time)+" where U = "+postgresString(name)+"")
      else:
            insertNewUser(name, "", "", "", time)

      databaseActions(1)
      return str(time)

def db_getTime(name):
      databaseActions(0)
      _,_,_,_,_, time = getRowValues(name)
      databaseActions(1)
      return time

def db_deleteUser(name):
      databaseActions(0)
      cur.execute("DELETE from USERINFO where u="+postgresString(name))
      databaseActions(1)

def databaseActions(state):
      if   state == 0:
            databaseConnection()
            global cur
            cur = con.cursor()
      elif state == 1:
            con.commit()  
            con.close()

def postgresString(editingString):
      return "'" + str(editingString) + "'"

def getRowValues(name):
      cur.execute("SELECT ID, U, LINK, BUILD_PATH,BUILD_NUMBER,MESSAGE_TIME from USERINFO")  
      rows = cur.fetchall()
      userId = 0
      for row in rows:
            userId   = row[0]
            if str(name) == row[1]:
                  return row[0], row[1], row[2], row[3], row[4], row[5]

      return userId, False, False, False, False, False

def isExist(name):
      _, nameInTable, _,_,_,_ = getRowValues(name)
      if str(name) == str(nameInTable):
            return True
      else:
            return False

def getNewIndex(name):
      userId, _,_,_,_,_ = getRowValues(name)
      if userId:
            return str(int(userId)+1)
      else:
            return "0" 

def insertNewUser(userName, link, path, number ,messageTime):
      localVar = {}
      for a,b in locals().items():
            localVar[a] = b
            if not localVar[a]:
                  localVar[a] = "some text"
      del localVar['localVar']

      print(localVar)

      cur.execute("INSERT INTO USERINFO (ID,U,LINK,BUILD_PATH,BUILD_NUMBER, MESSAGE_TIME) VALUES ("
                  +getNewIndex(localVar['userName'])+","+postgresString(localVar['userName'])+","+postgresString(localVar['link'])+","
                  +postgresString(localVar['path'])+","+postgresString(localVar['number'])+","+postgresString(localVar['messageTime'])+")")

