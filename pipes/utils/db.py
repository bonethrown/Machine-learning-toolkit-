from pymongo import Connection

MONGO_DB_HOST = 'localhost'
MONGO_DB_HOST_PORT = 27017
MONGO_DB_COLLECTION = 'nubunu_db'

def getConnection():
   connection = Connection(MONGO_DB_HOST, MONGO_DB_HOST_PORT)
   db = connection[MONGO_DB_COLLECTION]
   return db                
