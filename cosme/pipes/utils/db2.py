from pymongo import Connection

MONGO_DB_HOST = 'localhost'
MONGO_DB_HOST_PORT = 27017
MONGO_DB = 'comments_db'

MONGO_MIRROR1_HOST = '23.96.17.252'
MONGO_DB_HOST_PORT = 27017 




COMMENT_DB_PRIM = 'items'
COMMENT_DB_FALL = 'itemsTest'

MAIN_COLLETION = 'lalina'
BACKUP_COLLETION = 'testLalina'

BACKUP_DB = ''
def pureConnection(mongoHost = MONGO_DB_HOST, mongoPort = MONGO_DB_HOST_PORT):
    connection = Connection(mongoHost, mongoPort)
    return connection

def getConnection(mongoDatabase = MONGO_DB):
    connection = Connection(MONGO_DB_HOST, MONGO_DB_HOST_PORT)
    db = connection[mongoDatabase]
    return db 

def getOwnDb( mongoCollection = COMMENT_DB_FALL, mongoDatabase = MONGO_DB):
    connection = Connection(MONGO_DB_HOST, MONGO_DB_HOST_PORT)
    db = connection[mongoDatabase]
    db = db[mongoCollection]
    return db 

def anyConnection(mongoHost = MONGO_DB_HOST, mongoPort = MONGO_DB_HOST_PORT, database = MONGO_DB, collection = MAIN_COLLETION):
    connection = Connection(mongoHost, mongoPort)
    db = connection[database]
    db =db[collection]
    return db


