from pymongo import MongoClient

client = None
db = None
_db_ready = False

def init_db(uri):
    global client, db, _db_ready
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        # Trigger a connection attempt
        client.server_info()
        db = client.get_default_database()
        _db_ready = True
    except Exception:
        client = None
        db = None
        _db_ready = False

def get_collection(name):
    return db[name] if db is not None else None

def is_db_ready():
    return _db_ready
